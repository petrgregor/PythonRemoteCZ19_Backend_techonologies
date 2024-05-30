from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView

from viewer.models import *

from django.forms import *


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
        context["genre"] = Genre.objects.get(id=pk)
        context["movies"] = Movie.objects.filter(genres__id=pk)
        return context


class CreatorsListView(ListView):
    template_name = "creators.html"
    model = People
    context_object_name = "creators"


class CreatorTemplateView(TemplateView):
    template_name = "creator.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context["creator"] = People.objects.get(id=pk)
        return context


# Forms
class MovieForm(Form):
    title_orig = CharField(max_length=185)  # https://cs.wikipedia.org/wiki/Lopadotemachoselachogaleokranioleipsanodrimhypotrimmatosilphioparaomelitokatakechymenokichlepikossyphophattoperisteralektryonoptekephalliokigklopeleiolagoiosiraiobaphetraganopterygon
    title_cz = CharField(max_length=185, required=False)
    #countries = ModelChoiceField(queryset=Country)
    #directors = ModelChoiceField(queryset=People)
    #actors = ModelChoiceField(queryset=People)
    #genres = ModelChoiceField(queryset=Genre)
    length = IntegerField(min_value=1, required=False)
    rating = IntegerField(min_value=0, max_value=100, required=False)
    released = DateField()
    description = CharField(widget=Textarea, required=False)


"""
class MovieCreateView(FormView):
    template_name = 'form.html'
    form_class = MovieForm
"""


class MovieCreate(View):

    def get(self, request):
        if request.method == 'GET':
            title_orig = request.GET.get("title_orig")
            title_cz = request.GET.get("title_cz")
            length = request.GET.get("length")
            rating = request.GET.get("rating")
            released = request.GET.get("released")
            description = request.GET.get("description")
            Movie.objects.create(
                title_orig=title_orig,
                title_cz=title_cz,
                length=length,
                rating=rating,
                released=released,
                description=description
            )
        return movies(request)


class MovieModelForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieCreateView(CreateView):
    template_name = 'form.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('movies')
