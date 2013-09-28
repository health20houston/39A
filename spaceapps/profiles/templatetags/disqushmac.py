from django import template
from base64 import b64encode
import simplejson
import hashlib
import hmac
import time

register = template.Library()

@register.simple_tag
def disqus_hmac(**kwargs):
    secretkey = ''
    userid = kwargs['userid']
    fname = kwargs['fname']
    lname = kwargs['lname']
    email = kwargs['email']
    friendly_email = email.encode('utf-8')
    lowered_email = friendly_email.lower()
    data = simplejson.dumps({
        'id': userid.encode('utf-8'),
        'username': '%s %s' % (fname, lname),
        'email': lowered_email,
        'avatar': 'http://www.gravatar.com/avatar/' + hashlib.md5(lowered_email).hexdigest() + '.jpg',
    })
    timestamp = int(time.time())
    message = b64encode(data)
    encoded = hmac.HMAC(secretkey, '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()
    return '%s %s %s' % (message, encoded, timestamp)
