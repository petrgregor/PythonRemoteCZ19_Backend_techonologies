from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from viewer.models import *


def hello(request):
    return HttpResponse('Hello, world!')


# User data - Regular expression
def hello2(request, s):
    return HttpResponse(f'Hello, {s} world!')


# User data - URL encoding
def hello3(request):
    s = request.GET.get('s', '')
    return HttpResponse(f'Hello, {s} world!')


def hello4(request):
    adjectives = ['nice', 'beautiful', 'cruel', 'blue', 'green']
    context = {'adjectives': adjectives, 'name': 'Petr'}
    return render(
        request=request,  # předáváme na další stránku request (obsahuje např. data o přihlášeném uživateli)
        template_name="hello.html",
        context=context
    )


def home(request):
    return render(request, "home.html")


def movies(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, "movies.html", context)


def movie(request, pk):
    if Movie.objects.filter(id=pk).exists():
        movie = Movie.objects.get(id=pk)
        context = {'movie': movie}
        return render(request, "movie.html", context)
    return movies(request)
    #return reverse_lazy('movies')
