from django import forms

from .models import Rockets_bdf

class Rockets_bdfForm(forms.ModelForm):
    class Meta:
        model = Rockets_bdf
#        fields = '__all__'
        fields = ['text', 'start_rockets', 'kolichestvo_amort', 'zhestkost_amort']