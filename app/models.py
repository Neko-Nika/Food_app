from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    proteins = models.FloatField(blank=False, null=False)
    fats = models.FloatField(blank=False, null=False)
    carbohydrates = models.FloatField(blank=False, null=False)
    calories = models.IntegerField(blank=False, null=False)
