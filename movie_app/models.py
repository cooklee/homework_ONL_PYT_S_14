from django.db import models


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=123)
    last_name = models.CharField(max_length=123)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=123)


class Movie(models.Model):
    title = models.CharField(max_length=123)
    director = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='directed_by')
    screenplay = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='writen_by')
    year = models.IntegerField()
    rating = models.IntegerField()
    genre = models.ManyToManyField(Genre)
