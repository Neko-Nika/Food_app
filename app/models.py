from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    proteins = models.FloatField(blank=False, null=False)
    fats = models.FloatField(blank=False, null=False)
    carbohydrates = models.FloatField(blank=False, null=False)
    calories = models.IntegerField(blank=False, null=False)

class Step(models.Model):
    step = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True, null=True, default="")

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200, unique=False, blank=False, null=False)
    image = models.ImageField(upload_to='recipe_avatars/', default='recipe_avatars/no-photo.png', blank=True, null=True)
    likes = models.IntegerField(unique=False, blank=False, null=False, default=0)
    liked = models.ManyToManyField(User, related_name="liked_users")
    products = models.ManyToManyField(Product)
    steps = models.ManyToManyField(Step)
    amounts = ArrayField(models.IntegerField())

    total_proteins = models.FloatField(blank=False, null=False)
    total_fats = models.FloatField(blank=False, null=False)
    total_carbohydrates = models.FloatField(blank=False, null=False)
    total_calories = models.IntegerField(blank=False, null=False)
