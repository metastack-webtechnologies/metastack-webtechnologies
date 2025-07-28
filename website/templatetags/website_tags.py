# C:\Metastack-website\metaproducts-website\website\templatetags\website_tags.py

from django import template
from ..models import Service
import datetime

register = template.Library()

@register.simple_tag
def get_all_services():
    """
    A simple template tag to fetch all service objects.
    This is used to populate the services dropdown in the header on every page.
    """
    return Service.objects.all()

@register.simple_tag
def current_year():
    """
    Returns the current year.
    Used for the copyright notice in the footer.
    """
    return datetime.date.today().year

@register.filter(name='splitlines')
def splitlines(value):
    """
    Splits a string by newlines and returns a list of stripped lines.
    """
    if not isinstance(value, str):
        return value
    return [line.strip() for line in value.splitlines()]

@register.filter(name='strip')
def strip_filter(value):
    """
    Strips leading/trailing whitespace from a string.
    """
    if not isinstance(value, str):
        return value
    return value.strip()

@register.simple_tag(takes_context=True)
def is_active(context, view_name):
    request = context['request']
    if request.resolver_match and request.resolver_match.url_name == view_name:
        return 'nav-link-active'  # This is the CSS class for the active link
    return ''