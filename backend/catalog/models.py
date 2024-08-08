from django.db import models

class Product(models.Model):
    '''Продукт'''
    name = models.CharField(
        max_length=256,
        verbose_name='Название продукта'
    )
    image = models.ImageField(
        verbose_name='Изображение продукта',
        upload_to='products'
    )
    category = models.CharField(
        max_length=128,
        verbose_name='Категория'
    )
    fix_price = models.FloatField(
        verbose_name='Фиксированная цена за кг продукта'
    )
    stock = models.IntegerField(
        verbose_name='Остаток продукта в кг'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self):
        return self.name
