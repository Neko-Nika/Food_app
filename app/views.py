from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="/quickstart")
def index(request):
    return HttpResponse("HEllo")

def quickstart(request):
    return render(request, "quickstart.html")

