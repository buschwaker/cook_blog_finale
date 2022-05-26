from django import template
from django.core.cache import cache

from contact.models import Social, About

register = template.Library()


@register.simple_tag()
def get_social_links():
    socials = cache.get('socials')
    if not socials:
        socials = Social.objects.all()
        cache.set('socials', socials, 3600)
    return socials


@register.simple_tag()
def get_about():
    about = cache.get('about')
    if not about:
        about = About.objects.last()
        cache.set('about', about, 3600)
    return about
