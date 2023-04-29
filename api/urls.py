from django.urls import path

from . import views

urlpatterns = [
    path("create_account", views.create_account, name="create_account"),
    path('login_account', views.login_account, name="login_account"),
    path('create_new_recipe', views.create_new_recipe, name="create_new_recipe"),
    path('edit_recipe/<int:id>', views.edit_recipe, name="edit_recipe"),
    path('like_recipe', views.like_recipe, name="like_recipe"),
]