from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from PIL import Image


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

class Meal(models.Model):
    grams = models.IntegerField(blank=False, null=False)
    proteins = models.FloatField(blank=False, null=False)
    fats = models.FloatField(blank=False, null=False)
    carbohydrates = models.FloatField(blank=False, null=False)
    calories = models.IntegerField(blank=False, null=False)

    recipe = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)

class Day(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False, unique=False)

    total_proteins = models.FloatField(blank=False, null=False)
    total_fats = models.FloatField(blank=False, null=False)
    total_carbohydrates = models.FloatField(blank=False, null=False)
    total_calories = models.IntegerField(blank=False, null=False)
    water = models.FloatField(blank=False, null=False)
    
    breakfast = models.ManyToManyField(Meal, related_name='breakfast_set')
    lunch = models.ManyToManyField(Meal, related_name='lunch_set')
    dinner = models.ManyToManyField(Meal, related_name='dinner_set')
    snack = models.ManyToManyField(Meal, related_name='snack_set')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='recipe_avatars/no-photo.png', upload_to='profile_pics')
    weight = models.FloatField(default=0)
    isFree = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


class Reminders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.CharField(max_length=255)
    checked = models.BooleanField(default=True)

class Photos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos')

    def save(self, *args, **kwargs):
        super(Photos, self).save(*args, **kwargs)

        img = Image.open(self.photo.path)

        if img.height > 900 or img.width > 900:
            output_size = (900, 900)
            img.thumbnail(output_size)
            img.save(self.photo.path)