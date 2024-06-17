from rest_framework import serializers

from viewer.models import Movie, People


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        #fields = ['title_orig', 'title_cz', 'released', 'description']
        fields = '__all__'


"""
class MovieDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'
"""


class CreatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = People
        fields = '__all__'
