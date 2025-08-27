from django import template
from datetime import date, datetime
from django.utils.dateformat import format as dj_format

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_attribute(obj, attr_name):
    """
    A template filter to get an attribute from an object dynamically.
    Useful for iterating over an object's fields.
    """
    return getattr(obj, attr_name, '')

@register.filter
def format_date(value, fmt="Y-m-d"):
    """
    Format a date/datetime using Django's dateformat; if value is not a date,
    return it unchanged.
    """
    if isinstance(value, (date, datetime)):
        return dj_format(value, fmt)
    return value