from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import os
import json
from app.models import *


@csrf_exempt
def login_account(request):
    if request.method == "POST" and request.content_type == 'application/json':
        data = json.loads(request.body)
        
        password = data['password']
        username = data['username']

        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                raise Exception("Invalid email or password")
        except Exception as exc:
            response_data = {
                'success': False,
                'message': str(exc)
            }

            return JsonResponse(response_data) 

        response_data = {
            'success': True,
            'message': 'User signed in successfully'
        }

        return JsonResponse(response_data)
    else:

        response_data = {
            'success': False,
            'message': 'Only POST requests are allowed'
        }
        
        return JsonResponse(response_data, status=405)


@csrf_exempt
def create_account(request):
    if request.method == "POST" and request.content_type == 'application/json':
        data = json.loads(request.body)
        
        username = data['username']
        password = data['password']
        repeat_password = data['repeatpassword']
        email = data['email']
        first_name = data['firstname']
        last_name = data['lastname']

        try:
            if password != repeat_password:
                raise Exception("Passwords do not match")
            if User.objects.filter(username=username).first() is not None:
                raise Exception("User with this username already exists")
            if User.objects.filter(email=email).first() is not None:
                raise Exception("User with this email already exists")
        except Exception as exc:
            response_data = {
                'success': False,
                'message': str(exc)
            }

            return JsonResponse(response_data) 

        new_user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        new_user.save()

        login(request, new_user)

        response_data = {
            'success': True,
            'message': 'User registered successfully'
        }

        return JsonResponse(response_data)
    else:

        response_data = {
            'success': False,
            'message': 'Only POST requests are allowed'
        }
        
        return JsonResponse(response_data, status=405)
    

@csrf_exempt
@login_required
def create_new_recipe(request):
    if request.method == "POST":
        data = request.POST
        try:
            title = data["title"]
            total_proteins = float(data["total_proteins"])
            total_fats = float(data["total_fats"])
            total_carbohydrates = float(data["total_carbohydrates"])
            total_calories = int(float(data["total_calories"]))

            products = []
            amounts = []
            for pr in [x for x in data.keys() if x.startswith("product_")]:
                products.append(Product.objects.get(name=data[pr]))
                amounts.append(data['amount_' + pr])
            
            steps = []
            for st in [x for x in data.keys() if x.startswith("step_")]:
                step = Step.objects.create(step=data[st], description=data['description_' + st])
                step.save()
                steps.append(step)

            recipe = Recipe.objects.create(author=request.user, title=title, total_proteins=total_proteins,
                                           total_fats=total_fats, total_carbohydrates=total_carbohydrates, total_calories=total_calories,
                                           amounts=amounts)
            if 'image' in request.FILES:
                recipe.image = request.FILES['image']
            recipe.save()
            recipe.products.add(*products)
            recipe.steps.add(*steps)
            recipe.save()

            response_data = {
                'success': True,
                'message': 'Recipe was created'
            }

            return JsonResponse(response_data)
        
        except Exception as exc:
            response_data = {
                'success': False,
                'message': exc
            }

            return JsonResponse(response_data)
    else:

        response_data = {
            'success': False,
            'message': 'Only POST requests are allowed'
        }
        
        return JsonResponse(response_data, status=405)


@csrf_exempt
@login_required
def edit_recipe(request, id):
    if request.method == "POST":
        data = request.POST
        try:
            title = data["title"]
            total_proteins = float(data["total_proteins"])
            total_fats = float(data["total_fats"])
            total_carbohydrates = float(data["total_carbohydrates"])
            total_calories = int(float(data["total_calories"]))

            products = []
            amounts = []
            for pr in [x for x in data.keys() if x.startswith("product_")]:
                products.append(Product.objects.get(name=data[pr]))
                amounts.append(data['amount_' + pr])
            
            steps = []
            for st in [x for x in data.keys() if x.startswith("step_")]:
                step = Step.objects.create(step=data[st], description=data['description_' + st])
                step.save()
                steps.append(step)

            recipe = Recipe.objects.get(id=id)
            recipe.title = title
            recipe.total_proteins = total_proteins
            recipe.total_fats = total_fats
            recipe.total_carbohydrates = total_carbohydrates
            recipe.total_calories = total_calories

            if 'image' in request.FILES:
                recipe.image = request.FILES['image']
            recipe.save()

            recipe.products.clear()
            recipe.steps.clear()
            recipe.amounts = amounts

            recipe.products.add(*products)
            recipe.steps.add(*steps)
            recipe.save()

            response_data = {
                'success': True,
                'message': 'Recipe was updated'
            }

            return JsonResponse(response_data)
        
        except Exception as exc:
            response_data = {
                'success': False,
                'message': exc
            }

            return JsonResponse(response_data)
    else:

        response_data = {
            'success': False,
            'message': 'Only POST requests are allowed'
        }
        
        return JsonResponse(response_data, status=405)


@csrf_exempt
@login_required
def like_recipe(request):
    if request.method == "POST" and request.content_type == 'application/json':
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=int(data['user']))
            recipe = Recipe.objects.get(id=int(data['recipe']))

            if user in recipe.liked.all():
                recipe.liked.remove(user)
                recipe.likes -= 1
            else:
                recipe.liked.add(user)
                recipe.likes += 1

            recipe.save()
            
            response_data = {
                'success': True,
                'message': 'Recipe was updated'
            }

            return JsonResponse(response_data)
        
        except Exception as exc:
            response_data = {
                'success': False,
                'message': exc
            }

            return JsonResponse(response_data)
    else:

        response_data = {
            'success': False,
            'message': 'Only POST requests are allowed'
        }
        
        return JsonResponse(response_data, status=405)
