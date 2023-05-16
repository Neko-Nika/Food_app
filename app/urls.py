from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="default"),
    path("quickstart", views.quickstart, name="quickstart"),
    
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.signout, name="logout"),

    path("recipes", views.recipes, name="recipes"),
    path("create_recipe", views.create_recipe, name="create_recipe"),
    path("create_recipe/<int:id>", views.edit_recipe, name="edit_recipe"),
    path("recipe/<int:id>", views.recipe, name="recipe"),

    path("diary", views.diary, name="diary"),
    path("diary/<int:days>", views.diary_another, name="diary_another"),
]
