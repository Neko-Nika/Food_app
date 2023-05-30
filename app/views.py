from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

import app.models
from app.models import *


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
        'local_products': zip(obj.amounts, obj.products.all())
    }
    return render(request, "create_recipe.html", context)


def recipe(request, id):
    obj = Recipe.objects.get(id=id)
    context = {
        "recipe": obj,
        "products": zip(obj.amounts, obj.products.all())
    }
    return render(request, "recipe.html", context)


# рендерим страницу ЛК, если не авторизованы редирект на вход
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {'profile': get_object_or_404(app.models.Profile, user=request.user)}
    return render(request, 'profile.html', context)


def change_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        # если пришел пост запрос, обновляем данные в бд
        profile = get_object_or_404(app.models.Profile, user=request.user)
        # обновляем аву
        profile.avatar = request.FILES.get('avatar') if request.FILES.get('avatar') else profile.avatar
        # юзернэйм
        profile.user.username = request.POST.get('username') if request.POST.get('username') else profile.user.username
        # почту
        profile.user.email = request.POST.get('email') if request.POST.get('email') else profile.user.email
        # имя
        profile.user.first_name = request.POST.get('name') if request.POST.get('name') else profile.user.first_name
        # фамилию
        profile.user.last_name = request.POST.get('lastname') if request.POST.get(
            'lastname') else profile.user.last_name
        # сохраняем профиль
        profile.save()
        # сохраняем пользователя
        profile.user.save()
        return redirect('profile')
    # если другие методы, рендерим страницу
    return render(request, 'change_profile.html', {'profile': get_object_or_404(app.models.Profile, user=request.user)})


# аналогично change_profile, только теперь изменяем вес
def change_weight(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        # находим нашего пользователя в бд
        profile = get_object_or_404(app.models.Profile, user=request.user)
        # изменяем вес
        profile.weight = float(request.POST.get('weight')) if float(request.POST.get('weight')) > 0 else profile.weight
        profile.save()
        return redirect('profile')
    return render(request, 'change_weight.html', {'profile': get_object_or_404(app.models.Profile, user=request.user)})


def reminders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'PUT':
        # если ПУТ метод, выбираем наше напоминание и меняем значок активности
        # получаем атрибуты, которые пришли
        attr = request.body.decode().split('&')
        # получаем id
        id = int(attr[0].split('=')[1])
        # получаем значение чекбокса
        checked = int(attr[1].split('=')[1])
        # находим напоминание по id
        reminder = get_object_or_404(app.models.Reminders, id=id)
        # изменяем значение и сохраняем
        reminder.checked = True if checked == 1 else False
        reminder.save()
    return render(request, 'reminders.html',
                  {'reminders': app.models.Reminders.objects.filter(user=request.user).order_by('-id')})


def reminder(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'DELETE':
        # тут все понятно, удаляем напоминание
        get_object_or_404(app.models.Reminders, id=id).delete()
        return redirect('reminders')
    if request.method == 'POST':
        # обновляем данные напоминания
        r = get_object_or_404(app.models.Reminders, id=id)
        r.text = request.POST['text']
        r.date = request.POST.get('time') if request.POST.get('time') else r.date
        r.save()
        return redirect('reminders')
    # рендерим страницу
    return render(request, 'reminder.html', {'reminder': get_object_or_404(app.models.Reminders, id=id)})


def create_reminder(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        # если пост запрос
        data = request.POST  #
        reminder = app.models.Reminders()  # создаем экземпляр класса напоминаний
        # записываем данные
        reminder.text = data['Text']
        reminder.user = request.user
        reminder.date = data['date']
        reminder.save()  # сохраняем в бд
        return redirect('reminders')  # делаем редирект на страницу с напоминаниями
    # рендерим страницу с формой
    return render(request, 'create_reminder.html')


def photos(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'photos.html', {'photos': app.models.Photos.objects.filter(user=request.user)})


def photos_add(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        if request.FILES.get('photos'):
            for photo in request.FILES.getlist('photos'):
                app.models.Photos.objects.create(photo=photo, user=request.user)
        return redirect('photos')
    return render(request, 'add_photos.html', {})


def photos_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        get_object_or_404(app.models.Photos, id=id, user=request.user).delete()
        return redirect('photos')



def support(request):
    return render(request, 'support.html')


def support_success(request):
    return render(request, 'supp_succ.html')


def contacts(request):
    return render(request, 'contacts.html')
