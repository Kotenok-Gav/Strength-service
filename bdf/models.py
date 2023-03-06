from django.db import models
from django.contrib.auth.models import User


class Rockets_bdf(models.Model):
    #Формирование файла БДФ для ракеты
    #help_text="текст подсказка около поля"

    #Поля не вкл. в BDF
    text = models.CharField(max_length=200, null=True)                                   #Описание проекта
    data_added = models.DateTimeField(auto_now_add=True, null=True)           #время создания
    owner = models.ForeignKey(User, on_delete=models.CASCADE)                 #Привязка проектов к аккаунту

    #Поля вкл. в BDF
    start_rocket = models.PositiveSmallIntegerField(help_text="Введите 0, если старт подводный, 1 - наземный", null=True)   #Определение старта ракеты. Введите 0, если старт подводный, 1 - наземный
    kolichestvo_amort = models.PositiveSmallIntegerField(help_text="Введите число от 1 до 5")       #Количество поясов амортизации. Введите число от 1 до 5
    zhestkost_amort = models.DecimalField(decimal_places=2, max_digits=12, help_text="(с точностью до сотых) zhestkost_amort * 10^7")  #Задайте жесткость амортизатора (с точностью до сотых): \n zhestkost_amort * 10^7
    #X1 расстояние от нижнего края ракеты до верхнего (первого) пояса амортизации
    X1 = models.DecimalField(decimal_places=1, max_digits=6, help_text="от нижнего края ракеты до верхнего (первого) пояса амортизации в м с точностью до десятых")
    #X1 расстояние от нижнего края ракеты второго пояса амортизации
    X2 = models.DecimalField(decimal_places=1, max_digits=6, help_text="от нижнего края ракеты второго пояса амортизации в м с точностью до десятых")
    # V_sredy скорость набегающего потока
    V_sredy = models.DecimalField(decimal_places=1, max_digits=4, help_text="м/с")
    # d0 Диаметр ракеты
    d0 = models.DecimalField(decimal_places=2, max_digits=4, help_text="с точностью до сотых")
    #L Длина ракеты
    L = models.DecimalField(decimal_places=1, max_digits=4, help_text="с точностью до десятых")
    #m Стартовая масса ракеты
    m = models.DecimalField(decimal_places=1, max_digits=12, help_text="в кг.")

    def __str__(self):
        #Отображение названия модели
        return f"{self.text[:50]}"




