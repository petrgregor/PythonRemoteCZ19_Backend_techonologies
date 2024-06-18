from django.contrib import admin
from viewer.models import *

from django.contrib.admin import ModelAdmin


class MovieAdmin(ModelAdmin):

    @staticmethod
    def released_year(obj):
        return obj.released.year

    @staticmethod
    def cleanup_description(modeladmin, request, queryset):
        queryset.update(description=None)

    ordering = ['title_orig']
    list_display = ['id', 'title_orig', 'title_cz', 'released_year']
    list_display_links = ['id', 'title_orig', 'title_cz']
    list_per_page = 5
    list_filter = ['genres', 'countries', 'directors']
    search_fields = ['title_orig', 'title_cz']
    actions = ['cleanup_description']

    fieldsets = [
        (None, {'fields': ['title_orig', 'title_cz', 'countries', 'created']}),
        (
            'External Information',
            {
                'fields': ['directors', 'actors', 'genres', 'released', 'length'],
                'description': (
                    'These fields are going to be filled with data parsed '
                    'from external databases.'
                )
            }
        ),
        (
            'User Information',
            {
                'fields': ['rating', 'description'],
                'description': 'These fields are intended to be filled in by our users.'
            }
        )
    ]
    readonly_fields = ['created']


class PeopleAdmin(ModelAdmin):

    @staticmethod
    def capitalize_name_surname(modeladmin, request, queryset):
        for obj in queryset:
            obj.name = obj.name.capitalize()
            # TODO dopracovat

    ordering = ['surname', 'name']
    list_display = ['id', 'name', 'surname', 'country', 'current_age']
    list_display_links = ['id', 'name', 'surname']
    list_per_page = 10
    list_filter = ['country']
    search_fields = ['name', 'surname', 'biography']

    # TODO: fieldsets


admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(People, PeopleAdmin)
admin.site.register(Image)
admin.site.register(Review)
