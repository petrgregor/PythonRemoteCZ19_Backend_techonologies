"""hollymovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from viewer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello/', hello),
    path('hello2/<s>', hello2),
    path('hello3/', hello3),
    path('hello4/', hello4),

    path('', home, name='home'),
    #path('movies/', movies, name='movies'),  # funkcionální view
    #path('movies/', MoviesView.as_view(), name='movies'),  # class-based view: View class
    #path('movies/', MoviesTemplateView.as_view(), name='movies'),  # class-based view: TemplateView class
    path('movies/', MoviesListView.as_view(), name='movies'),  # class-based view: ListView class
    # path('movie/<pk>/', movie, name='movie'),  # function view
    #path('movie/<pk>/', MovieView.as_view(), name='movie'),  # CBV: View
    path('movie/<pk>/', MovieTemplateView.as_view(), name='movie'),  # CBV: TemplateView
    #path('genres/', genres, name='genres'),  # functional view
    #path('genres/', GenresView.as_view(), name='genres'),  # CBV: View
    #path('genres/', GenresTemplateView.as_view(), name='genres'),  # CBV: TemplateView
    path('genres/', GenresListView.as_view(), name='genres'),  # CBV: ListView
    #path('genre/<pk>/', genre, name='genre'),  # functional view
    #path('genre/<pk>/', GenreView.as_view(), name='genre'),  # CBV: View
    path('genre/<pk>/', GenreTemplateView.as_view(), name='genre'),  # CBV: TemplateView
    path('creators/', CreatorsListView.as_view(), name='creators'),
]
