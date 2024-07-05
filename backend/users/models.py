from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''Пользователь'''

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(
        verbose_name="Электронная почта",
        unique=True
    )
    first_name = models.CharField(
        max_length=15,
        verbose_name="Имя"
    )
    phone = models.CharField(
        max_length=15,
        verbose_name="Телефон"
    )
    address = models.CharField(
        max_length=50,
        verbose_name="Адрес"
    )
    image = models.ImageField(
        upload_to='users',
        null=True,
        blank=True,
        verbose_name="Изображение"
    )
    check_list = models.BooleanField(
        default=False,
        verbose_name="Согласие на обработку персональных данных"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Персонал"
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
