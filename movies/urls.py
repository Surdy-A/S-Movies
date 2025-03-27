from django.urls import path
from .views import MovieHome, movie_list, movie_detail, series_movie_detail, movie_reviews, search_movies, rate_movie
from django.conf.urls import handler404

app_name = 'movies'
handler404 = 'movies.views.custom_404_view'

urlpatterns = [
    path('', MovieHome, name='movie'),
    path('category/<str:cat>', movie_list, name='movie_list'),
    path('<int:id>/', movie_detail, name='movie_detail'),
    path('series/<int:movie_id>/', series_movie_detail, name='series_movie_detail'),
    path('help/', series_movie_detail, name='series_movie_detail'),
    path('movie/<int:movie_id>/reviews/', movie_reviews, name='movie_reviews'),
    path('search/', search_movies, name='search_movies'),
    path("rate/<int:movie_id>/", rate_movie, name="rate_movie"),
]

# GenuineRashy@8229
