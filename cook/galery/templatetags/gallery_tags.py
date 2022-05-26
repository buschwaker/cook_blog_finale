from django import template
from django.core.cache import cache

from galery.models import Photo

register = template.Library()


@register.inclusion_tag('blog/include/tags/gallery_tag.html')
def get_gallery():
    photos = cache.get('photos')
    if not photos:
        number = Photo.objects.count()
        number_4 = number % 4
        photos_to_show = number - number_4
        photos = Photo.objects.order_by('id')[:photos_to_show]
        cache.set('photos', photos, 3600)
    return {'photos': photos}
