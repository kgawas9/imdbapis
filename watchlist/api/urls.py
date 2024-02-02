from django.urls import path

from watchlist.api import views
from watchlist.api.views import MovieListAPIView

urlpatterns = [
    # path('movies/', views.movie_list, name='list-of-movies'),
    path('movies/', MovieListAPIView.as_view(), name='list-of-movies'),
    path('movies/<int:pk>/', views.get_movie_details, name='get-movie-details'),
]