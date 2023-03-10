from django.db import models
from django.contrib.auth.models import User


class Rockets_bdf(models.Model):
    #Формирование файла БДФ для ракеты
    #help_text="текст подсказка около поля"
    #verbose_name='Напишите что нибудь'

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
    #Масса ГЧ
    m_gch = models.DecimalField(decimal_places=1, max_digits=12, help_text="в кг.")
    #расстояние от нижнего края ракеты до точки приложения массы ГЧ
    X_gch = models.DecimalField(decimal_places=1, max_digits=12, help_text="в м с точностью до десятых")
    #Масса СУ ракеты
    m_cy = models.DecimalField(decimal_places=1, max_digits=12, help_text="в кг.")
    #расстояние от нижнего края ракеты до точки приложения массы СУ
    X_cy = models.DecimalField(decimal_places=1, max_digits=12, help_text="в м с точностью до десятых")
    #масса ДУ ракеты
    m_dy = models.DecimalField(decimal_places=1, max_digits=12, help_text="в кг.")
    #расстояние от нижнего края ракеты до точки приложения массы ДУ
    X_dy = models.DecimalField(decimal_places=1, max_digits=12, help_text="в м с точностью до десятых")
    #масса окислителя
    mo = models.DecimalField(decimal_places=1, max_digits=12, help_text="в кг.")
    #Длина бака окислителя
    Lo = models.DecimalField(decimal_places=1, max_digits=12, help_text="в м с точностью до десятых")
    #расстояние от нижнего края ракеты до нижнего днища бака окислителя
    Xo = models.DecimalField(decimal_places=1, max_digits=12, help_text="в м с точностью до десятых")
    # масса горючего
    mg = models.DecimalField(decimal_places=1, max_digits=12, help_text="в кг.")
    # Длина бака горючего
    Lg = models.DecimalField(decimal_places=1, max_digits=12, help_text="в м с точностью до десятых")
    # Расстояние от нижнего края ракеты до нижнего днища бака горючего
    Xg = models.DecimalField(decimal_places=1, max_digits=12, help_text="в м с точностью до десятых")
    #Задание свойства материала ракеты. Модуль Юнга
    modul_unga1 = models.DecimalField(decimal_places=1, max_digits=12, help_text="в м с точностью до десятых", verbose_name='Задание свойства материала ракеты. Модуль Юнга')
    #Коэффициент Пуассона
    koeff_puass1 = models.DecimalField(decimal_places=2, max_digits=6, help_text="с точностью до сотых", verbose_name='Коэффициент Пуассона')
    #Задание свойства материала контейнера. Модуль Юнга
    modul_unga2 = models.DecimalField(decimal_places=1, max_digits=12, help_text="в м с точностью до десятых", verbose_name='Задание свойства материала контейнера. Модуль Юнга')
    #Коэффициент Пуассона
    koeff_puass2 = models.DecimalField(decimal_places=2, max_digits=6, help_text="с точностью до сотых", verbose_name='Коэффициент Пуассона')
    #Плотность материала контейнера
    plotnost2 = models.DecimalField(decimal_places=2, max_digits=6, help_text="с точностью до сотых", verbose_name='Плотность материала контейнера')
    #Введите время выхода ракеты из контейнера в секундах
    t = models.DecimalField(decimal_places=3, max_digits=6, help_text="с точностью до тысячных", verbose_name='Время выхода ракеты из контейнера в секундах')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для первой точки
    t_p1 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для первой точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее первому времени значение тяги
    P1 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее первому времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для второй точки
    t_p2 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для второй точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее второму времени значение тяги
    P2 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее второму времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для третьей точки
    t_p3 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для третьей точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее третьему времени значение тяги
    P3 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее третьему времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для четвертой точки
    t_p4 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для четвертой точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее четвертому времени значение тяги
    P4 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее четвертому времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для пятой точки
    t_p5 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для пятой точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее пятому времени значение тяги
    P5 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее пятому времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для шестой точки
    t_p6 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для шестой точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее шестому времени значение тяги
    P6 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее шестому времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для седьмой точки
    t_p7 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для седьмой точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее седьмому времени значение тяги
    P7 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее седьмому времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для восьмой точки
    t_p8 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для восьмой точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее восьмому времени значение тяги
    P8 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее восьмому времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для девятой точки
    t_p9 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для девятой точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее девятому времени значение тяги
    P9 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее девятому времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для десятой точки
    t_p10 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для десятой точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее десятому времени значение тяги
    P10 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее десятому времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для одиннадцатой точки
    t_p11 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для одиннадцатой точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее одиннадцатому времени значение тяги
    P11 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее одиннадцатому времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для двенадцатой точки
    t_p12 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для двенадцатой точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее двенадцатому времени значение тяги
    P12 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее двенадцатому времени значение тяги')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время в секундах для тринадцатой точки
    t_p13 = models.DecimalField(decimal_places=2, max_digits=6, help_text="в секундах с точностью до сотых", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите время для тринадцатой точки')
    #Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее тринадцатому времени значение тяги
    P13 = models.IntegerField(help_text="в Н (в диапазоне от 100 до 99'999'999 Н)", verbose_name='Задание тяги двигателя (13 точек) в зависисмости от времени. Введите соответствующее тринадцатому времени значение тяги')







    def __str__(self):
        #Отображение названия модели
        return f"{self.text[:50]}"




