from django import template
import datetime

register = template.Library()

@register.filter
def unix_to_date(value):
    try:
        return datetime.datetime.fromtimestamp(value).strftime('%B %d, %Y')
    except (ValueError, TypeError):
        return value