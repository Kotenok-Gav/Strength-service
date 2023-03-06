from django import forms
from django.core.exceptions import ValidationError

from .models import Rockets_bdf

class Rockets_bdfForm(forms.ModelForm):
    #initial="начальное значение для поля при его отображении"
    #label="указывает текст перед формой"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label="Название проекта"
        self.fields['text'].initial="Ангара"
        self.fields['start_rocket'].label="Определение старта ракеты"
        self.fields['start_rocket'].initial="0"
        self.fields['kolichestvo_amort'].label = "Количество поясов амортизации"
        self.fields['kolichestvo_amort'].initial = "1"
        self.fields['zhestkost_amort'].label = "Жесткость амортизатора"
        self.fields['zhestkost_amort'].initial = "6.56"
        self.fields['X1'].label = "Введите расстояние"
        self.fields['X1'].initial = "3.2"
        self.fields['X2'].label = "Введите расстояние"
        self.fields['X2'].initial = "3.7"
        self.fields['V_sredy'].label = "Скорость набегающего потока"
        self.fields['V_sredy'].initial = "50.8"
        self.fields['d0'].label = "Диаметр ракеты"
        self.fields['d0'].initial = "6.33"
        self.fields['L'].label = "Длина ракеты"
        self.fields['L'].initial = "25.3"
        self.fields['m'].label = "Стартовая масса ракеты"
        self.fields['m'].initial = "100000.3"

    class Meta:
        model = Rockets_bdf
        fields = ['text', 'start_rocket', 'kolichestvo_amort', 'zhestkost_amort', 'X1', 'X2', 'V_sredy', 'd0', 'L', 'm']

    def clean_start_rocket(self):
        start_rocket = self.cleaned_data['start_rocket']
        if start_rocket > 1 or start_rocket < 0:
            raise ValidationError('Указали неверное значение')
        return start_rocket

    def clean_kolichestvo_amort(self):
        kolichestvo_amort = self.cleaned_data['kolichestvo_amort']
        if kolichestvo_amort > 5 or kolichestvo_amort < 1:
            raise ValidationError('Указали неверное значение')
        return kolichestvo_amort
