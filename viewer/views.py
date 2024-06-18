from concurrent.futures._base import LOGGER

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView, DetailView
from django_addanother.views import CreatePopupMixin
from django_addanother.widgets import AddAnotherWidgetWrapper

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


@login_required
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

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        #if context["form_review"].is_valid():
        # FIXME: každý uživatel by měl hodnotit maximálně jednou
        Review.objects.create(movie=context["movie"],
                              user=Profile.objects.get(user=request.user),
                              rating=request.POST.get("rating"),
                              text=request.POST.get("text")
                              )
        return render(request, "movie.html", context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        movie_ = Movie.objects.get(id=pk)
        context["movie"] = movie_
        context["images"] = Image.objects.filter(movie=movie_)
        context["reviews"] = Review.objects.filter(movie=movie_)
        context["form_review"] = ReviewModelForm
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
"""
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

"""
class MovieCreateView(FormView):
    template_name = 'form.html'
    form_class = MovieForm
"""

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
"""


def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Value must be capitalized.')


class PastMonthField(DateField):

    def validate(self, value):
        super().validate(value)
        if value >= date.today():
            raise ValidationError('Only past dates allowed here.')

    def clean(self, value):
        result = super().clean(value)
        return date(year=result.year, month=result.month, day=1)


class MovieModelForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
        #fields = ['title_cz', 'title_orig']
        #exclude = ['title_cz']
        #exclude = []
        widgets = {
            'directors': AddAnotherWidgetWrapper(
                SelectMultiple,
                reverse_lazy('creator_create')
            )
        }

    rating = IntegerField(min_value=0, max_value=100, required=False)
    length = IntegerField(min_value=1, required=False)
    released = DateField(widget=NumberInput(attrs={'type': 'date'}))

    def clean_title_orig(self):
        initial = self.cleaned_data['title_orig']
        return initial.strip()

    def clean_title_cz(self):
        initial = self.cleaned_data['title_cz']
        return initial.strip()

    """def clean(self):
        pass"""


class MovieCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('movies')
    permission_required = 'viewer.add_movie'

    def form_invalid(self, form):
        LOGGER.warning('Invalid data in MovieCreateView.')
        return super().form_invalid(form)


# TODO: MovieUpdateView
# TODO: MovieDeleteView


class PeopleForm(Form):
    name = CharField(max_length=32)
    surname = CharField(max_length=32, required=False)
    date_of_birth = DateField(required=False)
    date_of_death = DateField(required=False)
    place_of_birth = CharField(max_length=64, required=False)
    place_of_death = CharField(max_length=64, required=False)
    country = ModelChoiceField(queryset=Country.objects)
    biography = CharField(widget=Textarea, required=False)

    def clean_name(self):
        #initial_data = super().clean()  # původní data od uživatele ve formuláři
        #initial_name = initial_data['name']  # původní name od uživatele
        initial_name = self.cleaned_data['name']  # původní name od uživatele
        return initial_name.strip().capitalize()  # odstraníme prázdné znaky na začátku a konci textu + zvětšíme první znak

    def clean(self):
        initial_data = super().clean()
        if initial_data['date_of_birth'] and initial_data['date_of_death']:
            if initial_data['date_of_birth'] >= initial_data['date_of_death']:
                raise ValidationError("Date of death must be after date of birth.")
        return initial_data


class PeopleCreateFormView(FormView):
    template_name = 'form.html'
    form_class = PeopleForm
    success_url = reverse_lazy('creators')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        People.objects.create(
            name=cleaned_data['name'],
            surname=cleaned_data['surname'],
            date_of_birth=cleaned_data['date_of_birth'],
            date_of_death=cleaned_data['date_of_death'],
            place_of_birth=cleaned_data['place_of_birth'],
            place_of_death=cleaned_data['place_of_death'],
            country=cleaned_data['country'],
            biography=cleaned_data['biography']
        )
        return result

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class PeopleModelForm(ModelForm):
    class Meta:
        model = People
        fields = '__all__'

    #date_of_birth = DateField(widget=SelectDateWidget)
    date_of_birth = DateField(widget=NumberInput(attrs={'type': 'date'}))
    date_of_death = DateField(widget=NumberInput(attrs={'type': 'date'}))

    def clean_name(self):
        initial_name = self.cleaned_data['name']  # původní name od uživatele
        return initial_name.strip().capitalize()  # odstraníme prázdné znaky na začátku a konci textu + zvětšíme první znak

    def clean_surname(self):
        initial_surname = self.cleaned_data['surname']  # původní name od uživatele
        return initial_surname.strip().capitalize()  # odstraníme prázdné znaky na začátku a konci textu + zvětšíme první znak

    def clean(self):
        initial_data = super().clean()
        try:
            if initial_data['date_of_birth'] and initial_data['date_of_death']:
                if initial_data['date_of_birth'] >= initial_data['date_of_death']:
                    raise ValidationError("Date of death must be after date of birth.")
        except KeyError:
            pass
        return initial_data


class PeopleCreateView(PermissionRequiredMixin, CreatePopupMixin, CreateView):
    template_name = 'form_creator.html'
    form_class = PeopleModelForm
    success_url = reverse_lazy('creators')
    permission_required = 'viewer.add_people'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class PeopleUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form_creator.html'
    model = People
    form_class = PeopleModelForm
    success_url = reverse_lazy('creators')
    permission_required = 'viewer.change_people'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a creator.')
        return super().form_invalid(form)


## Authorization test
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class PeopleDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'creator_confirm_delete.html'
    model = People
    success_url = reverse_lazy('creators')
    permission_required = 'viewer.delete_people'


# TODO: GenreCreateView
# TODO: GenreUpdateView
# TODO: GenreDeleteView

# TODO: CountryCreateView
# TODO: CountryUpdateView
# TODO: CountryDeleteView


class ImageModelForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'


class ImageCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form_image.html'
    form_class = ImageModelForm
    success_url = reverse_lazy('home')
    permission_required = 'viewer.add_image'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)

# TODO: ImageUpdateView
# TODO: ImageDeleteView

# TODO: mazání obrázků z adresáře: https://timonweb.com/django/cleanup-files-and-images-on-model-delete-in-django/


class ImageDetailView(DetailView):
    model = Image
    template_name = 'image.html'


class ReviewModelForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
