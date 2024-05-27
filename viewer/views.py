from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView

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


def genres(request):
    genres = Genre.objects.all()
    context = {'genres': genres}
    return render(request, "genres.html", context)


def genre(request, pk):
    genre = Genre.objects.get(id=pk)
    movies = Movie.objects.filter(genre__id=pk)
    context = {'genre': genre, 'movies': movies}
    return render(request, "movies_by_genre.html", context)


# CBV: Class-Based Views
## View class
class MoviesView(View):
    def get(self, request):
        movies = Movie.objects.all()
        context = {'movies': movies}
        return render(request, "movies.html", context)


## TemplateView class
class MoviesTemplateView(TemplateView):
    template_name = "movies.html"
    extra_context = {'movies': Movie.objects.all()}


## ListView class
class MoviesListView(ListView):
    template_name = "movies2.html"
    model = Movie
    # pozor: do template se posílá jako object_list


# přepsat všechna stávající funkční view (mimo hello...) na CBV:
# movie
class MovieView(View):
    def get(self, request, pk):
        if Movie.objects.filter(id=pk).exists():
            movie = Movie.objects.get(id=pk)
            context = {'movie': movie}
            return render(request, "movie.html", context)
        return movies(request)


class MovieTemplateView(TemplateView):
    template_name = "movie.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context["movie"] = Movie.objects.get(id=pk)
        return context


# genres
class GenresView(View):
    def get(self, request):
        genres = Genre.objects.all()
        context = {'genres': genres}
        return render(request, "genres.html", context)


class GenresTemplateView(TemplateView):
    template_name = "genres.html"
    extra_context = {'genres': Genre.objects.all()}


class GenresListView(ListView):
    template_name = "genres.html"
    model = Genre

    # 1. způsob, jak předefinovat 'object_list' v contextu:
    """def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context"""

    # 2. způsob, jak předefinovat 'object_list' v contextu:
    context_object_name = 'genres'


# genre
class GenreView(View):
    def get(self, request, pk):
        genre = Genre.objects.get(id=pk)
        movies = Movie.objects.filter(genre__id=pk)
        context = {'genre': genre, 'movies': movies}
        return render(request, "movies_by_genre.html", context)


class GenreTemplateView(TemplateView):
    template_name = "movies_by_genre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context["movies"] = Movie.objects.filter(genre__id=pk)
        return context
