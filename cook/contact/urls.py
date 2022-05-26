from django.urls import path
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [

    path(
        'contact/',
        cache_page(3600*24)(views.ContactView.as_view()),
        name='contact'
    ),
    path('feedback/', views.CreateContact.as_view(), name='feedback'),
    path(
        'about/',
        cache_page(3600*24)(views.AboutView.as_view()),
        name='about'
    ),
]
