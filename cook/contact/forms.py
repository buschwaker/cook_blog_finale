from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import ContactModel


class ContactForms(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'
        labels = {
            'name': _('Имя'),
            'email': _('E-mail'),
            'website': _('Сайт'),
            'message': _('Сообщение'),
        }
