from django.db.models import *  #(Model, CharField, ForeignKey, DO_NOTHING,
                                #IntegerField, DateField, TextField, DateTimeField)


class Genre(Model):
    name = CharField(max_length=16, null=False, blank=False)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"<Genre: {self.name}>"

    def __str__(self):
        return f"{self.name}"

    def movies_count(self):
        return self.movies.all().count()


class Country(Model):
    name = CharField(max_length=64, null=False, blank=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name}"


class People(Model):
    name = CharField(max_length=32)
    surname = CharField(max_length=32)
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
        return f"{self.name} {self.surname} ({self.date_of_birth.year})"


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
        return f"{self.title_orig} ({self.released})"

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


