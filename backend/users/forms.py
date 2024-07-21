from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser


class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Пожалуйста, введите правильную электронную почту и пароль. Оба поля могут быть чувствительны к регистру.",
        'inactive': "Этот аккаунт не активен.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Электронная почта'
        self.fields['password'].label = 'Пароль'


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Такая электронная почта уже существует.')
        return email

class CustomUserChangeForm(UserChangeForm):
    password=None
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'phone', 'address', 'image', 'check_list')
