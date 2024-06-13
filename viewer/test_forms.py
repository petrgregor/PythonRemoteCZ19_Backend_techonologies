import datetime

from django.test import TestCase

from viewer.models import *
from viewer.views import PeopleModelForm


class PeopleFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Country.objects.create(name="Czech")
        Country.objects.create(name="Slovak")
        Country.objects.create(name="Germany")

    def test_people_form_is_valid(self):
        form = PeopleModelForm(
            data={
                'name': '   martin   ',
                'surname': 'novák',
                'date_of_birth': '1965-09-17', #datetime.date(1999, 2, 5).__str__(),
                'date_of_death': '2024-05-05', #datetime.date(2024,5,5).__str__(),
                'place_of_birth': 'Praha',
                'place_of_death': ' ',
                'country': '1',
                'biography': 'Nějaký text'
            }
        )
        print(f"\ntest_people_form_is_valid: {form.data}")
        self.assertTrue(form.is_valid())

    def test_people_date_form_is_invalid(self):
        form = PeopleModelForm(
            data={
                'name': '   martin   ',
                'surname': 'Novák',
                'date_of_birth': '1965-09-17', #datetime.date(1999, 2, 5).__str__(),
                'date_of_death': '1924-05-05', #datetime.date(2024,5,5).__str__(),
                'place_of_birth': 'Praha',
                'place_of_death': ' ',
                'country': '1',
                'biography': 'Nějaký text'
            }
        )
        print(f"\ntest_people_date_form_is_invalid: {form.data}")
        self.assertFalse(form.is_valid())

# pokud je vazba ManyToMany, pak se zadává seznam: 'genres': ['1', '2']

# TODO: MovieFormTest
