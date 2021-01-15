import random
import string
from django import template

register = template.Library()

@register.filter
def random_slugs(value):
	return '{}/{}/{}'.format(value, random.randint(1,100), ''.join(random.choices(string.ascii_letters, k=random.randint(5,10))))