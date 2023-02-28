from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from bdf.models import Rockets_bdf
from .forms import Rockets_bdfForm


def index(request):
    # домашня страница приложения bdf
    return render(request, 'bdf/index.html')


@login_required()
def rockets_bdf_all(request):
    # выводит все проекты
    rockets_bdf_all = Rockets_bdf.objects.filter(owner=request.user).all()
    context = {'rockets_bdf_all': rockets_bdf_all}
    return render(request, 'bdf/rockets_bdf_all.html', context)


@login_required()
def rocket(request, rocket_id):
    # выводит один проект
    rocket = Rockets_bdf.objects.get(id=rocket_id)
    #проверка того что тема принадлежит текущему пользователю
    if rocket.owner != request.user:
        raise Http404
    context = {"rocket": rocket}
    return render(request, 'bdf/rocket.html', context)


@login_required()
def rocket_bdf_new(request):
    #Создаем новый проект
    if request.method != 'POST':
        #Данные не отправляются, создается пустая форма
        form = Rockets_bdfForm
    else:
        #Отправлены данные POST, форма заполняется
        form = Rockets_bdfForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
#            form.save()
            return redirect('bdf:rockets_bdf_all')

    context = {'form': form}
    return render(request, 'bdf/rocket_bdf_new.html', context)


def rocket_bdf_edit(request, rocket_id):
    #редактируем существующий проект
    bdf_edit = Rockets_bdf.objects.get(id=rocket_id)

    if request.method != 'POST':
        #Исходный запрос, форма заполняется данными текущей записи
        form = Rockets_bdfForm(instance=bdf_edit)

    else:
        #Отправка данных POST
        form = Rockets_bdfForm(instance=bdf_edit, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bdf:rocket', rocket_id=bdf_edit.id)

    context = {'bdf_edit' : bdf_edit, 'form': form}
    return render(request, 'bdf/rocket_bdf_edit.html', context)
