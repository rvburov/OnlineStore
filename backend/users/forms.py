from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

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
