from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from movie_app.models import Movie, Person, Genre, Starring


# Create your views here.
def movies_view(request):
    movies = Movie.objects.order_by('-year')
    lang = request.COOKIES.get('lang', 'Not set')
    session_sort = request.session.get('sort')
    sort = request.GET.get('sort')
    if sort is None:
        sort = session_sort
    if sort == 'rosnaco':
        movies = movies.order_by('rating')
    elif sort == 'malejaco':
        movies = movies.order_by('-rating')
    else:
        movies = movies.order_by('-year')
    if sort is not None:
        request.session['sort'] = sort

    return render(request, 'movie_app/movies.html', {'movies': movies, 'lang': lang, 'sort': sort})


def movie_search(request):
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    title = request.GET.get('title', '')
    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')

    persons = Person.objects.filter(first_name__icontains=first_name,
                                    last_name__icontains=last_name)

    year_from = request.GET.get('year_from', 0)
    year_to = request.GET.get('year_to', 9999)
    if year_from == "":
        year_from = 0
    if year_to == "":
        year_to = 9999

    rating_form = request.GET.get('rating_from', 0)
    rating_to = request.GET.get('rating_to', 9999)
    if rating_form == "":
        rating_form = 0
    if rating_to == "":
        rating_to = 9999
    genres_lst = request.GET.getlist('genre')

    movies = movies.filter(title__icontains=title)
    q1 = Q(director__in=persons)
    q2 = Q(screenplay__in=persons)
    movies = movies.filter(q1 | q2)
    movies = movies.filter(year__gte=year_from)
    movies = movies.filter(year__lte=year_to)
    movies = movies.filter(rating__gte=rating_form)
    movies = movies.filter(rating__lte=rating_to)
    for genre in genres_lst:
        movies = movies.filter(genre__in=[genre])

    return render(request, 'movie_app/movies_search.html', {'genres': genres, 'movies': movies})


def movie_view(request, id):
    movie = Movie.objects.get(pk=id)
    return render(request, 'movie_app/movie.html', {'movie': movie})


def add_actor_to_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    persons = Person.objects.all()
    if request.method == 'GET':
        return render(request, 'movie_app/add_actor_to_movie_form.html', {'movie': movie, 'persons': persons})
    person_id = request.POST.get('person')
    person = Person.objects.get(pk=person_id)
    role = request.POST.get('role')
    s = Starring()
    s.movie = movie
    s.person = person
    s.role = role
    s.save()
    return redirect('add_actor', movie_id)


def persons_view(request):
    persons = Person.objects.all()
    messages = request.session.get('messages', [])
    if 'messages' in request.session:
        del request.session['messages']
    return render(request, 'movie_app/person.html', {'persons': persons,
                                                     'messages': messages})


def person_create_view(request):
    if request.method == 'GET':
        return render(request, 'movie_app/create_person_form.html')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    Person.objects.create(first_name=first_name, last_name=last_name)
    request.session['messages'] = ['Udało sie dodać osobe']
    return redirect('person_list')
class CreatePersonView(View):
    def get(self, request):
        return render(request, 'movie_app/create_person_form.html')
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        Person.objects.create(first_name=first_name, last_name=last_name)
        request.session['messages'] = ['Udało sie dodać osobe']
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
