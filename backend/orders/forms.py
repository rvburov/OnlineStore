from django import forms
from django.utils import timezone
import datetime
import pytz
from .models import Order


def get_min_time():
    moscow_tz = pytz.timezone('Europe/Moscow')
    min_time = timezone.now().astimezone(moscow_tz) + datetime.timedelta(hours=1)
    return min_time.strftime('%Y-%m-%dT%H:%M')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['id', 'name', 'phone', 'address', 'time', 'check_list']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите ваше имя',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+7 (***) ***-**-**',
                'required': 'required',
                'pattern': '\+7\(\d{3}\)\d{3}-\d{2}-\d{2}',
                'title': 'Введите номер телефона в формате +7(XXX)XXX-XX-XX',
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Город, улица, дом, квартира',
                'required': 'required'
            }),
            'time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'placeholder': 'Выберите дату и время',
                'required': 'required',
                'min': get_min_time(),
            }),
            'check_list': forms.CheckboxInput(attrs={
                'required': 'required'
            }),
        }

    def clean_time(self):
        selected_time = self.cleaned_data['time']
        moscow_tz = pytz.timezone('Europe/Moscow')
        min_time = timezone.now().astimezone(moscow_tz) + datetime.timedelta(hours=1)
        if selected_time < min_time:
            raise forms.ValidationError(f'Дата и время доставки не могут быть раньше {min_time.strftime("%Y-%m-%d %H:%M")}')
        return selected_time
