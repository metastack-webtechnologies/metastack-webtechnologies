from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='splitlines')
def splitlines(value):
    """
    Splits a string by newlines and returns a list of stripped lines.
    Useful for displaying features entered one per line in a TextField.
    """
    if not isinstance(value, str):
        return value
    return [line.strip() for line in value.splitlines()]

@register.filter(name='strip')
def strip_filter(value):
    """
    Strips leading/trailing whitespace from a string.
    Ensures no extra spaces affect display, especially after splitting lines.
    """
    if not isinstance(value, str):
        return value
    return value.strip()