from django.shortcuts import render


def error_404(request, exception):
    return render(request, 'handlers/404.html')
