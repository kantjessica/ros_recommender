from django import template

register = template.Library()

@register.filter(name='genId')
def genId(str):
	return str[7:]