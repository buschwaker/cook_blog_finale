from math import ceil

from django import template
from django.core.cache import cache

from blog.models import Category, Post

register = template.Library()


def get_all_categories():
    return Category.objects.all()


@register.simple_tag()
def get_list_category():
    return get_all_categories()


@register.inclusion_tag('blog/include/tags/top_menu.html')
def get_categories():
    category = get_all_categories
    return {"list_category": category}


@register.inclusion_tag('blog/include/tags/recipes_tag.html')
def get_last_post():
    list_last_post = cache.get('list_last_post')
    if not list_last_post:
        list_last_post = Post.objects.select_related(
            "category"
        ).order_by("-id")[:5]
        cache.set('list_last_post', list_last_post, 60)
    return {"list_last_post": list_last_post}


@register.filter(name='truncate_text')
def truncate_text(value, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    if len(arg_list) == 2:
        text = value.rsplit(" ")[int(arg_list[0]):int(arg_list[1])]
        return (" ".join(text) + '...').capitalize()
    elif len(arg_list) == 1:
        text = value.rsplit(" ")[int(arg_list[0]):]
        return (" ".join(text)).capitalize()


@register.filter(name='read_speed')
def read_speed(value):
    words_per_minute = 150
    post = value
    recipe = (
        str(recipe.ingredients) + str(recipe.directions)
        for recipe in post.recipe.all()
    )
    recipe_text = ""
    for i in recipe:
        recipe_text += i
    text = post.text + recipe_text
    count = len(text.split()) / words_per_minute
    return str(ceil(count)) + ' мин. чтения'


@register.filter(name='comment_word')
def comment_word(value):
    if value == 0:
        word = 'нет комментариев'
    elif 5 <= value <= 20:
        word = f'{value} комментариев'
    else:
        if value % 10 == 1:
            word = f'{value} комментарий'
        elif value % 10 == 2 or value % 10 == 3 or value % 10 == 4:
            word = f'{value} комментария'
        else:
            word = f'{value} комментариев'
    return word
