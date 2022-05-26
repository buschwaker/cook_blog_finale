from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField
)
from django.contrib.auth import get_user_model, password_validation
from django import forms
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class CreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Введите пароль'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Подтвердите пароль'
                                          }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta(UserCreationForm.Meta):

        model = User
        fields = ('username', 'email', 'avatar')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введите имя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Введите e-mail'
                                             }),
            'avatar': forms.ClearableFileInput(),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Введите имя'
                                      }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Введите пароль'}),
    )
