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
    path("profile", views.profile, name="profile"),
    path("change-profile", views.change_profile, name="change-profile"),
    path("change-weight", views.change_weight, name="change-weight"),
    path("reminders", views.reminders, name="reminders"),
    path("reminder/<int:id>", views.reminder, name="reminder"),
    path("create-reminder", views.create_reminder, name="create-reminder"),
]
