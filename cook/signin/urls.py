from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from .forms import LoginForm
from . import views

app_name = 'signin'

urlpatterns = [
    path(
      'logout/',
      LogoutView.as_view(),
      name='logout'
    ),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'login/', LoginView.as_view(
            template_name='blog/home.html',
            extra_context={"login_context": True},
            form_class=LoginForm
        ),
        name='login'
    ),
]
