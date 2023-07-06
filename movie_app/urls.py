"""
URL configuration for homework_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from movie_app import views

urlpatterns = [
    path('movies/', views.movies_view, name='movie_list'),
    path('movies_search', views.movie_search, name='movie_list'),
    path('movie_create/', views.movie_create_view, name='movie_create'),
    path('movies_edit/<int:id>/', views.movie_edit_view, name='movie_edit'),
    path('persons/', views.persons_view, name='person_list'),
    path('person_add/', views.person_create_view, name='person_create'),
    path('persons/<int:id>/', views.person_edit_view, name='person_edit'),
    path('movies/<int:id>/', views.movie_view, name='movie_detail'),
    path('movies/<int:movie_id>/addActor/', views.add_actor_to_movie, name='add_actor'),
]
