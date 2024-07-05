from django.db import models
from users.models import CustomUser


class Order(models.Model):
    '''Заказ'''
    ORDER_STATUS_CHOICES = (
        ('waiting', 'Ожидание доставки'),
        ('delivered', 'Доставлено'),
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name = 'Пользователь',
    )
    name = models.CharField(
        max_length=20,
        verbose_name='Имя',
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=16,
        verbose_name='Телефон',
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=50,
        verbose_name='Адрес',
        null=True,
        blank=True,
    )
    check_list = models.BooleanField(
        verbose_name='Согласие на обработку персональных данных',
        null=True,
        blank=True,
    )
    time = models.DateTimeField(
        verbose_name='Дата и время доставки',
        null=True,
        blank=True,

    )
    status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS_CHOICES,
        default='waiting',
        verbose_name='Статус заказа',
    )
    delivery_price = models.FloatField(
        verbose_name='Цена за доставку',
        default=0
    )
    total_price = models.FloatField(
        verbose_name='Итоговая цена',
        default=0
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}'


class OrderItem(models.Model):
    '''Корзина заказа'''
    order = models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
        related_name='order_item',
        verbose_name = 'Данные заказа',
    )
    product_name = models.CharField(
        max_length=256,
        verbose_name='Название продукта',
        null=True,
    )
    product_weight = models.FloatField(
        verbose_name='Вес продукта',
        default=0
    )
    product_price = models.FloatField(
        verbose_name='Цена продукта',
        default=0
    )
    product_image = models.ImageField(
        verbose_name = 'Изображение продукта',
        null=True, 
        blank=True,
    )

    class Meta:
        verbose_name = 'Корзина заказа'
        verbose_name_plural = 'Корзина заказов'

    def __str__(self):
        return f'Корзина заказа {self.id}'
