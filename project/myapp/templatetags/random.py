import random
import string

from django import template

register = template.Library()


@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)


@register.simple_tag
def random_slug(l=10):
    slug = ''.join(random.choices(string.ascii_lowercase + string.digits, k=l))
    return slug
