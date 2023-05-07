from django import template

register = template.Library()

@register.filter
def replace_string(value, args):
    search, replace = args.split(',')
    return value.replace(search, replace)

