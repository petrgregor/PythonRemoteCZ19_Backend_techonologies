from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse('Hello, world!')


# User data - Regular expression
def hello2(request, s):
    return HttpResponse(f'Hello, {s} world!')


# User data - URL encoding
def hello3(request):
    s = request.GET.get('s', '')
    return HttpResponse(f'Hello, {s} world!')
