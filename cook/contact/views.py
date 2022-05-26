from django.shortcuts import render
from django.views.generic import CreateView
from django.views import View
from django.core.mail import send_mail

from .forms import ContactForms
from .models import ContactLink, About


class ContactView(View):
    def get(self, request):
        contacts = ContactLink.objects.all()
        form = ContactForms()
        return render(
            request,
            'contact/contact.html',
            {'contacts': contacts, 'form': form}
        )


class CreateContact(CreateView):
    form_class = ContactForms
    success_url = '/'

    def form_valid(self, form):
        send_mail(
            f'Комментарий от {form.instance.name}',
            f'{form.instance.message}',
            'akroshko1995@gmail.com',
            ['akroshko1995@gmail.com'],
            fail_silently=True
        )
        self.object = form.save()
        return super().form_valid(form)


class AboutView(View):
    def get(self, request):
        about = About.objects.last()
        return render(request, 'contact/about.html', {'about': about})
