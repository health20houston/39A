from django import template
import random

register = template.Library()

@register.filter
def greeting(value)
    words = [hola, bounjour]
    return random.choice(words)
