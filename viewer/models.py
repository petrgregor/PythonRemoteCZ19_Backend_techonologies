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


class Movie(Model):
    title_orig = CharField(max_length=185, null=False, blank=False)  # https://cs.wikipedia.org/wiki/Lopadotemachoselachogaleokranioleipsanodrimhypotrimmatosilphioparaomelitokatakechymenokichlepikossyphophattoperisteralektryonoptekephalliokigklopeleiolagoiosiraiobaphetraganopterygon
    #genre = ForeignKey(Genre, on_delete=DO_NOTHING)
    genres = ManyToManyField(Genre, blank=True, related_name='movies')
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

