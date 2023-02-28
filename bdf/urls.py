from django.urls import path

from . import views

app_name = 'bdf'

urlpatterns = [
    #домашняя страница
    path('', views.index, name='index'),
    #список всех проектов
    path('rockets_bdf_all/', views.rockets_bdf_all, name='rockets_bdf_all'),
    #страница с отдельным проектом
    path('rockets_bdf_all/<int:rocket_id>/', views.rocket, name='rocket'),
    #страница для добвления новой темы
    path('rocket_bdf_new/', views.rocket_bdf_new, name='rocket_bdf_new'),
]