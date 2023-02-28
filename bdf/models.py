from django.db import models
from django.contrib.auth.models import User


class Rockets_bdf(models.Model):
    #Формирование файла БДФ для ракеты


    text = models.CharField(max_length=200, null=True, help_text='Введите описание проекта')    #Описание проекта
    data_added = models.DateTimeField(auto_now_add=True, null=True)                             #время создания
    start_rockets = models.SmallIntegerField()                                                  #Определение старта ракеты. Введите 1, если старт наземный, 0 - подводный
    kolichestvo_amort = models.SmallIntegerField()                                              #Количество поясов амортизации. Введите число от 2 до 5
    zhestkost_amort = models.DecimalField(decimal_places=2, max_digits=8)                       #Задайте жесткость амортизатора (с точностью до сотых): \n zhestkost_amort * 10^7
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        #Отображение названия модели
        return f"{self.text[:50]}..."




