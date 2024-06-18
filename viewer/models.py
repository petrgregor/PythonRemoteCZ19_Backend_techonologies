from datetime import date

from django.db.models import *  #(Model, CharField, ForeignKey, DO_NOTHING,

from accounts.models import Profile


#IntegerField, DateField, TextField, DateTimeField)


class Genre(Model):
    name = CharField(max_length=16, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"<Genre: {self.name}>"

    def __str__(self):
        return f"{self.name}"

    def movies_count(self):
        return self.movies.all().count()


class Country(Model):
    name = CharField(max_length=64, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name}"


class People(Model):
    name = CharField(max_length=32)
    surname = CharField(max_length=32, null=True, blank=True)
    date_of_birth = DateField(null=True, blank=True)
    date_of_death = DateField(null=True, blank=True)
    place_of_birth = CharField(max_length=64, null=True, blank=True)
    place_of_death = CharField(max_length=64, null=True, blank=True)
    country = ForeignKey(Country, null=True, on_delete=SET_NULL)
    biography = TextField(null=True, blank=True)

    class Meta:
        ordering = ['surname', 'name', 'date_of_birth']
        verbose_name_plural = 'People'

    def __str__(self):
        result = ""
        if self.name:
            result += self.name
        if self.surname:
            result += " " + self.surname
        if self.date_of_birth:
            result += f" ({self.date_of_birth.year})"
        return result

    # andrej
    def calculate_age(self):
        if self.date_of_birth is None:
            return None
        if self.date_of_death:
            end_date = self.date_of_death
        else:
            end_date = date.today()
        age = end_date.year - self.date_of_birth.year - ((end_date.month, end_date.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    # jiri
    @property
    def current_age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (
                today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return age


class Movie(Model):
    title_orig = CharField(max_length=185, null=False, blank=False)  # https://cs.wikipedia.org/wiki/Lopadotemachoselachogaleokranioleipsanodrimhypotrimmatosilphioparaomelitokatakechymenokichlepikossyphophattoperisteralektryonoptekephalliokigklopeleiolagoiosiraiobaphetraganopterygon
    title_cz = CharField(max_length=185, null=True, blank=False)
    countries = ManyToManyField(Country, blank=True, related_name='movies')
    directors = ManyToManyField("viewer.People", blank=True, related_name='directs')
    actors = ManyToManyField(People, blank=True, related_name='acts')
    #genre = ForeignKey(Genre, on_delete=DO_NOTHING)
    genres = ManyToManyField(Genre, blank=True, related_name='movies')
    length = IntegerField(null=True, blank=True)
    rating = IntegerField(null=True, blank=True)
    released = DateField()
    description = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title_orig']

    def __repr__(self):
        return f"<Movie: {self.title_orig}>"

    def __str__(self):
        return f"{self.title_orig} ({self.released.year})"

    def print_genres(self):
        result = ""
        for genre in self.genres.all():
            result += f"{genre}, "
        return result[:-2]

    def print_countries(self):
        result = ""
        for country in self.countries.all():
            result += f"{country}, "
        return result[:-2]

    def print_directors(self):
        result = ""
        for director in self.directors.all():
            result += f"{director}, "
        return result[:-2]

    def print_actors(self):
        result = ""
        for actor in self.actors.all():
            result += f"{actor}, "
        return result[:-2]


class Image(Model):
    image = ImageField(upload_to='images/', default=None, null=False, blank=False)
    movie = ForeignKey(Movie, on_delete=SET_NULL, null=True, blank=True)
    actors = ManyToManyField(People, blank=True, related_name='images')
    description = TextField(null=True, blank=True)

    def __repr__(self):
        return f"Image(image={self.image}, movie={self.movie}, actors={self.actors}, description={self.description})"

    def __str__(self):
        return f"Image: {self.image}, {self.description}"


class Review(Model):
    movie = ForeignKey(Movie, on_delete=CASCADE, null=False, blank=False)
    user = ForeignKey(Profile, on_delete=SET_NULL, null=True, blank=False)
    rating = IntegerField(null=True, blank=True)
    text = TextField(null=True, blank=True)

    def __repr__(self):
        return (f"Review(movie={self.movie}, user={self.user}, "
                f"rating={self.rating}, text={self.text})")

    def __str__(self):
        return f"User: {self.user}, movie:{self.movie}, rating={self.rating}, text={self.text[:50]}"
