from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path(
        'comment/<int:pk>/',
        views.CreateComment.as_view(),
        name="create_comment"
    ),
    path('', cache_page(5)(views.HomeView.as_view()), name="home"),
    path('<slug:slug>/', views.PostListView.as_view(), name="post_list"),
    path(
        '<slug:slug>/<slug:post_slug>/',
        views.PostDetailView.as_view(),
        name="post_single"
    )
]
