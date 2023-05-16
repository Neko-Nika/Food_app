from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from app.models import *

import datetime


@login_required(login_url="/quickstart")
def index(request):
    return redirect('recipes')


def quickstart(request):
    if request.user.is_authenticated:
        return redirect('default')

    return render(request, "quickstart.html")


def register(request):
    return render(request, "register.html")


def login(request):
    return render(request, "login.html")


@login_required(login_url="/login")
def signout(request):
    logout(request)
    return redirect("quickstart")


def recipes(request):
    context = {
        'recipes': Recipe.objects.all().order_by("-likes")
    }
    return render(request, "recipes.html", context)


@login_required(login_url="login")
def create_recipe(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, "create_recipe.html", context)


@login_required(login_url="login")
def edit_recipe(request, id):
    obj = Recipe.objects.get(id=id)
    context = {
        "recipe": obj,
        'products': Product.objects.all(),
        'local_products': zip(obj.amounts, obj.products.all().order_by("id"))
    }
    return render(request, "create_recipe.html", context)


def recipe(request, id):
    obj = Recipe.objects.get(id=id)
    context = {
        "recipe": obj,
        "products": zip(obj.amounts, obj.products.all().order_by("id"))
    }
    return render(request, "recipe.html", context)


@login_required(login_url="login")
def diary(request):
    recipes = Recipe.objects.all()
    products = Product.objects.all()

    liked = request.user.liked_users.all()
    mine = request.user.recipe_set.all()
    grams = [sum(x.amounts) for x in recipes]
    
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    try:
        day = Day.objects.get(author=request.user, date=today)
    except Day.DoesNotExist:
        day = None
    
    context = {
        'products': products,
        'recipes': zip(recipes, grams),
        'liked': liked,
        'mine': mine,
        'day': day,
        'date': today
    }

    return render(request, "diary.html", context)


@login_required(login_url="login")
def diary_another(request, days):
    if days == 0:
        return redirect('diary')

    recipes = Recipe.objects.all()
    products = Product.objects.all()

    liked = request.user.liked_users.all()
    mine = request.user.recipe_set.all()
    grams = [sum(x.amounts) for x in recipes]
    
    other_day = (datetime.datetime.today() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    try:
        day = Day.objects.get(author=request.user, date=other_day)
    except Day.DoesNotExist:
        day = None

    context = {
        'products': products,
        'recipes': zip(recipes, grams),
        'liked': liked,
        'mine': mine,
        'day': day,
        'date': other_day
    }

    return render(request, "diary.html", context)
