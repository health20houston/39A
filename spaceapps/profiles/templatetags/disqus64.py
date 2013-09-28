from django import template
from base64 import b64encode
import simplejson

register = template.Library()

@register.simple_tag
def disqus_b64(**kwargs):
    userid = kwargs['userid']
    username = kwargs['username']
    email = kwargs['email']
    data = simplejson.dumps({
        'id': userid.encode('utf-8'),
        'username': username.encode('utf-8'),
        'email': email.encode('utf-8'),
    })
    return b64encode(data)
