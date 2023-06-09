from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.db.models import Sum

import app.models
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

#рендерим страницу ЛК, если не авторизованы редирект на вход
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {'profile': get_object_or_404(app.models.Profile, user=request.user)}
    return render(request, 'profile.html', context)


def change_profile(request):
    if request.method == 'POST':
        #если пришел пост запрос, обновляем данные в бд
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
        profile.user.last_name = request.POST.get('lastname') if request.POST.get('lastname') else profile.user.last_name
        # сохраняем профиль
        profile.save()
        # сохраняем пользователя
        profile.user.save()
        return redirect('profile')
    #если другие запросы, рендерим страницу
    return render(request, 'change_profile.html', {'profile': get_object_or_404(app.models.Profile, user=request.user)})


#аналогично change_profile, только теперь изменяем вес
def change_weight(request):
    if request.method == 'POST':
        # находим нашего пользователя в бд
        profile = get_object_or_404(app.models.Profile, user=request.user)
        # изменяем вес
        profile.weight = float(request.POST.get('weight')) if float(request.POST.get('weight')) > 0 else profile.weight
        profile.save()
        return redirect('profile')
    return render(request, 'change_weight.html', {'profile': get_object_or_404(app.models.Profile, user=request.user)})



def reminders(request):
    if request.method == 'PUT':
        attr = request.body.decode().split('&')
        id = int(attr[0].split('=')[1])
        checked = int(attr[1].split('=')[1])
        reminder = get_object_or_404(app.models.Reminders, id=id)
        reminder.checked = True if checked == 1 else False
        reminder.save()
    if request.GET.get('id'):
        if request.method == 'DELETE':
            id = int(request.GET.get('id'))
            get_object_or_404(app.models.Reminders, id=id).delete()
            return redirect('/reminders')
        id = int(request.GET.get('id'))
        return render(request, 'reminder.html', {'reminder': get_object_or_404(app.models.Reminders, id=id)})
    return render(request, 'reminders.html', {'reminders': app.models.Reminders.objects.filter(user=request.user).order_by('-id')})


def reminder(request, id):
    if request.method == 'DELETE':
        get_object_or_404(app.models.Reminders, id=id).delete()
        return redirect('reminders')
    if request.method == 'POST':
        r = get_object_or_404(app.models.Reminders, id=id)
        r.text = request.POST['text']
        r.date = request.POST.get('time') if request.POST.get('time') else r.date
        r.save()
        return redirect('reminders')
    return render(request, 'reminder.html', {'reminder': get_object_or_404(app.models.Reminders, id=id)})


def create_reminder(request):
    if request.method == 'POST':
        data = request.POST
        reminder = app.models.Reminders()
        reminder.text = data['Text']
        reminder.user = request.user
        reminder.date = data['date']
        reminder.save()
        return redirect('reminders')
    elif request.method == 'DELETE':
        pass
    return render(request, 'create_reminder.html')

# Отчеты
@login_required(login_url="login")
def report(request):
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    try:
        day = Day.objects.get(author=request.user, date=today)
        # Считаем сумму калорий всех блюд завтрака (далее та же схема для других приемов пищи)
        breakfast   = day.breakfast.all().aggregate(Sum('calories'))['calories__sum']
        lunch       = day.lunch.all().aggregate(Sum('calories'))['calories__sum']
        dinner      = day.dinner.all().aggregate(Sum('calories'))['calories__sum']
        snack       = day.snack.all().aggregate(Sum('calories'))['calories__sum']
    except Day.DoesNotExist:
        day = None
        breakfast = None
        lunch = None
        dinner = None
        snack = None
    context = {
            "date":         today,      # Для начального значения календаря
            "today":        today,      # Для минимального значения календаря
            "day":          day,        # Данные по БЖУ и калориям за указанный день
            "breakfast":    breakfast,  # Калории на завтрак
            "lunch":        lunch,      # обед
            "dinner":       dinner,     # ужин
            "snack":        snack,      # перекус
    }
    return render(request, "report.html", context)

@login_required(login_url="login")
def report_another(request, days):
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    if days == 0:
        return redirect("report")
    other_day = (datetime.datetime.today() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    try:
        day = Day.objects.get(author=request.user, date=other_day)
        breakfast   = day.breakfast.all().aggregate(Sum('calories'))['calories__sum']
        lunch       = day.lunch.all().aggregate(Sum('calories'))['calories__sum']
        dinner      = day.dinner.all().aggregate(Sum('calories'))['calories__sum']
        snack       = day.snack.all().aggregate(Sum('calories'))['calories__sum']
    except Day.DoesNotExist:
        day = None
        breakfast = None
        lunch = None
        dinner = None
        snack = None
    context = {
        "date":         other_day,      # Начальная дата для календаря
        "today":        today,          # Минимальное значение
        "day":          day,
        "breakfast":    breakfast,
        "lunch":        lunch,
        "dinner":       dinner,
        "snack":        snack,
    }
    return render(request, "report.html", context)
