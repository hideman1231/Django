import random
from django import template

register = template.Library()

@register.filter
def random_numbers(value):
	return '{}/{}'.format(value, random.randint(1,100))
