from django.http import HttpResponse
from django.shortcuts import render, redirect

from movie_app.models import Movie, Person, Genre


# Create your views here.
def movies_view(request):
    movies = Movie.objects.order_by('-year')
    return render(request, 'movie_app/movies.html', {'movies': movies})


def movie_view(request, id):
    movie = Movie.objects.get(pk=id)
    return render(request, 'movie_app/movie.html', {'movie': movie})


def persons_view(request):
    persons = Person.objects.all()
    return render(request, 'movie_app/person.html', {'persons': persons})


def person_create_view(request):
    if request.method == 'GET':
        return render(request, 'movie_app/create_person_form.html')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    Person.objects.create(first_name=first_name, last_name=last_name)
    return redirect('person_list')


def person_edit_view(request, id):
    person = Person.objects.get(pk=id)
    if request.method == 'GET':
        return render(request, 'movie_app/create_person_form.html', {'person': person})
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    person.first_name = first_name
    person.last_name = last_name
    person.save()
    return redirect('person_edit', id)


def create_edit_movie(request, movie=None):
    if movie is None:
        movie = Movie()
    title = request.POST.get('title')
    year = request.POST.get('year')
    rating = request.POST.get('rating')
    director_id = request.POST.get('director')
    screenplay_id = request.POST.get('screenplay')
    genre = request.POST.getlist('genre')
    movie.title = title
    movie.year = year
    movie.director = Person.objects.get(pk=director_id)
    movie.screenplay = Person.objects.get(pk=screenplay_id)
    movie.rating = rating
    movie.save()
    movie.genre.set(genre)
    return movie

def movie_edit_view(request, id):
    movie = Movie.objects.get(pk=id)
    if request.method == 'GET':
        return render(request, 'movie_app/movie_form.html', {
            'movie': movie, 'persons': Person.objects.all(),
            'genres': Genre.objects.all()
        })
    create_edit_movie(request, movie)
    return redirect('movie_list')


def movie_create_view(request):
    if request.method == 'GET':
        return render(request, 'movie_app/movie_form.html', {
            'persons': Person.objects.all(),
            'genres': Genre.objects.all()
        })
    create_edit_movie(request)
    return redirect('movie_list')

