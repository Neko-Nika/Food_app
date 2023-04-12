from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import os
import json
from app.models import *


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
    