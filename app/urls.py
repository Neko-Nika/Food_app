from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="default"),
    path("quickstart", views.quickstart, name="default"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
]
