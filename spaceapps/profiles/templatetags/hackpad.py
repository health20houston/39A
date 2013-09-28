from django import template
import oauth2
import time

register = template.Library()

@register.simple_tag
def hackpad(**kwargs):
    fname = kwargs['fname'].encode('utf-8')
    lname = kwargs['lname'].encode('utf-8')
    email = kwargs['email'].encode('utf-8')
    padId = kwargs['padId']
    friendly_email = email.encode('utf-8')
    lowered_email = friendly_email.lower()
    api_method = "https://spaceapps.hackpad.com/ep/api/embed-pad";
    # 0-leg OAUTH
    params = {
        'oauth_version': "1.0",
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': int(time.time()),
        'email': lowered_email,
        'name' : fname + ' ' + lname,
        'padId': padId
        }
    consumer = oauth2.Consumer(key="", secret="")
    params['oauth_consumer_key'] = consumer.key
    req = oauth2.Request(method='GET', url=api_method, parameters=params)
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, None)
    return req.to_url()
