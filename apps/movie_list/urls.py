from django.urls import path

from apps.movie_list.views.movies import MovieIndexView


urlpatterns = [
    path('movies/', MovieIndexView.as_view(), name='movie_index'),
]
