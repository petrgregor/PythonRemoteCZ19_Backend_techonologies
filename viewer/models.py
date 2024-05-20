from django.db import models
from django.db.models import Model, CharField


class Genre(Model):
    name = CharField(max_length=16)
