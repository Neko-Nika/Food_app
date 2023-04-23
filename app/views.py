from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from app.models import Product


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
    return render(request, "recipes.html")

@login_required
def create_recipe(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, "create_recipe.html", context)