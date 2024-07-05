from django.db import models
from catalog.models import Product
from users.models import CustomUser


class Cart(models.Model):
    '''Корзина'''
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    products = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='cart',
        verbose_name = 'Продукты',
    )
    weight = models.FloatField(
        verbose_name = 'Вес продукта',
        default=0
    )
    price = models.FloatField(
        verbose_name='Стоимость продукта',
        default=0
    )


    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return self.products.name
    
