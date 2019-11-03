from django.urls import include, path

from apps.movie_list.urls import urlpatterns as movie_list_urlpatterns


urlpatterns = [
    path('', include(movie_list_urlpatterns)),
]
