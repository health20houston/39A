from django import template
import hashlib

register = template.Library()

@register.filter
def md5(value):
    """Encodes string in to md5"""
    friendly = value.encode('utf-8')
    lowered = friendly.lower()
    return hashlib.md5(lowered).hexdigest()
