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
