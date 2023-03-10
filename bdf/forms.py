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
        self.fields['m_gch'].label = "Масса ГЧ"
        self.fields['m_gch'].initial = "10000.3"
        self.fields['X_gch'].label = "Расстояние от нижнего края ракеты до точки приложения массы ГЧ"
        self.fields['X_gch'].initial = "2.3"
        self.fields['m_cy'].label = "Масса СУ ракеты"
        self.fields['m_cy'].initial = "10000.3"
        self.fields['X_cy'].label = "Расстояние от нижнего края ракеты до точки приложения массы СУ"
        self.fields['X_cy'].initial = "3.3"
        self.fields['m_dy'].label = "Масса ДУ ракеты"
        self.fields['m_dy'].initial = "10000.3"
        self.fields['X_dy'].label = "Расстояние от нижнего края ракеты до точки приложения массы ДУ"
        self.fields['X_dy'].initial = "3.3"
        self.fields['mo'].label = "Масса окислителя"
        self.fields['mo'].initial = "10000.3"
        self.fields['Lo'].label = "Длина бака окислителя"
        self.fields['Lo'].initial = "4.3"
        self.fields['Xo'].label = "Расстояние от нижнего края ракеты до нижнего днища бака окислителя"
        self.fields['Xo'].initial = "1.3"
        self.fields['mg'].label = "Масса горючего"
        self.fields['mg'].initial = "10000.3"
        self.fields['Lg'].label = "Длина бака горючего"
        self.fields['Lg'].initial = "2.3"
        self.fields['Xg'].label = "Расстояние от нижнего края ракеты до нижнего днища бака горючего"
        self.fields['Xg'].initial = "1.3"
        self.fields['modul_unga1'].initial = "1.3"
        self.fields['koeff_puass1'].initial = "6.33"
        self.fields['modul_unga2'].initial = "1.3"
        self.fields['koeff_puass2'].initial = "6.33"
        self.fields['plotnost2'].initial = "6.33"
        self.fields['t'].initial = "6.457"
        self.fields['t_p1'].initial = "6.45"
        self.fields['P1'].initial = "457830"
        self.fields['t_p2'].initial = "6.45"
        self.fields['P2'].initial = "457830"
        self.fields['t_p3'].initial = "6.45"
        self.fields['P3'].initial = "457830"
        self.fields['t_p4'].initial = "6.45"
        self.fields['P4'].initial = "457830"
        self.fields['t_p5'].initial = "6.45"
        self.fields['P5'].initial = "457830"
        self.fields['t_p6'].initial = "6.45"
        self.fields['P6'].initial = "457830"
        self.fields['t_p7'].initial = "6.45"
        self.fields['P7'].initial = "457830"
        self.fields['t_p8'].initial = "6.45"
        self.fields['P8'].initial = "457830"
        self.fields['t_p9'].initial = "6.45"
        self.fields['P9'].initial = "457830"
        self.fields['t_p10'].initial = "6.45"
        self.fields['P10'].initial = "457830"
        self.fields['t_p11'].initial = "6.45"
        self.fields['P11'].initial = "457830"
        self.fields['t_p12'].initial = "6.45"
        self.fields['P12'].initial = "457830"
        self.fields['t_p13'].initial = "6.45"
        self.fields['P13'].initial = "457830"
        self.fields['N'].initial = "67.4"

    class Meta:
        model = Rockets_bdf
        fields = ['text', 'start_rocket', 'kolichestvo_amort', 'zhestkost_amort', 'X1', 'X2', 'V_sredy', 'd0', 'L', 'm', 'm_gch', 'X_gch', 'm_cy', 'X_cy', 'm_dy', 'X_dy', 'mo', 'Lo', 'Xo', 'mg', 'Lg', 'Xg', 'modul_unga1', 'koeff_puass1', 'modul_unga2', 'koeff_puass2', 'plotnost2', 't', 't_p1', 'P1', 't_p2', 'P2', 't_p3', 'P3', 't_p4', 'P4', 't_p5', 'P5', 't_p6', 'P6', 't_p7', 'P7', 't_p8', 'P8', 't_p9', 'P9', 't_p10', 'P10', 't_p11', 'P11', 't_p12', 'P12', 't_p13', 'P13', 'N']

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

    def clean(self):
        super().clean()
        errors = {}
        if self.cleaned_data['m'] - self.cleaned_data['m_gch'] - self.cleaned_data['m_cy'] - self.cleaned_data['m_dy'] - self.cleaned_data['mo'] - self.cleaned_data['mg'] < 0:
            errors['m'] = ValidationError('НЕ ВЕРНО! СТАРТОВАЯ МАССА МЕНЬШЕ СУММЫ СОСРЕДОТОЧЕННЫХ МАСС И МАСС КОМПОНЕНТОВ!')
        if errors:
            raise ValidationError(errors)



