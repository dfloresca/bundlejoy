from django import template
from urllib.parse import urlparse

register = template.Library()

@register.filter
def ensure_scheme(url):
    parsed = urlparse(url)
    if parsed.scheme:
        return url
    else:
        return 'https://' + url

