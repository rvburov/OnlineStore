from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomLoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

class LoginView(View):
    """Обрабатывает страницу входа пользователя."""
    template_name = 'users/login.html'

    def get(self, request):
        form = CustomLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('users:account')
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    """Обрабатывает выход пользователя из системы."""
    def get(self, request):
        auth_logout(request)
        return render(request, 'users/logout.html')

class PasswordChangeView(LoginRequiredMixin, View):
    """Обрабатывает смену пароля пользователя."""
    template_name = 'users/password_change.html'
    
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('users:password_change_done')
        return render(request, self.template_name, {'form': form})

class PasswordChangeDoneView(LoginRequiredMixin, View):
    """Отображает страницу, подтверждающую успешную смену пароля."""
    template_name = 'users/password_change_done.html'
    
    def get(self, request):
        return render(request, self.template_name)

class PasswordResetView(View):
    """Обрабатывает запрос на сброс пароля."""
    template_name = 'users/password_reset.html'
    
    def get(self, request):
        form = PasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            form.save(request=request, email_template_name='users/password_reset_email.html')
            return redirect('users:password_reset_done')
        return render(request, self.template_name, {'form': form})

class PasswordResetDoneView(View):
    """Отображает страницу, подтверждающую успешный запрос на сброс пароля."""
    template_name = 'users/password_reset_done.html'
    
    def get(self, request):
        return render(request, self.template_name)

class PasswordResetConfirmView(View):
    """Обрабатывает подтверждение сброса пароля по ссылке из email."""
    template_name = 'users/password_reset_confirm.html'
    
    def get(self, request, uidb64=None, token=None):
        """Отображает форму для ввода нового пароля, если токен действителен."""
        try:
            UserModel = get_user_model()
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                form = SetPasswordForm(user=user)
                return render(request, self.template_name, {'form': form})
            else:
                return HttpResponse('Invalid token')
        
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            return HttpResponse('Invalid link')

    def post(self, request, uidb64=None, token=None):
        """Обрабатывает отправку формы для установки нового пароля, если токен действителен."""
        try:
            UserModel = get_user_model()
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                form = SetPasswordForm(user=user, data=request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('users:password_reset_complete')
                else:
                    return render(request, self.template_name, {'form': form})
            else:
                return HttpResponse('Invalid token')
        
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            return HttpResponse('Invalid link')

class PasswordResetCompleteView(View):
    """Отображает страницу, подтверждающую успешное завершение сброса пароля."""
    template_name = 'users/password_reset_complete.html'
    
    def get(self, request):
        return render(request, self.template_name)

class AccountView(LoginRequiredMixin, View):
    """Отображает страницу с информацией о пользователях."""
    template_name = 'users/account.html'

    def get(self, request):
        accounts = CustomUser.objects.all()
        return render(request, self.template_name, {'accounts': accounts})

class AccountAddView(View):
    """Регистрация нового пользователя."""
    template_name = 'users/account_add.html'
    
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('users:account')
        return render(request, self.template_name, {'form': form})

class AccountDeleteView(LoginRequiredMixin, View):
    """Удаление аккаунта пользователя."""
    template_name = 'users/account_delete.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        user.delete()
        return redirect(reverse_lazy('users:login'))

class AccountUpdateView(LoginRequiredMixin, View):
    """Обновление данных аккаунта пользователя."""
    template_name = 'users/account_update.html'

    def get(self, request):
        form = CustomUserChangeForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:account')
        return render(request, self.template_name, {'form': form})
