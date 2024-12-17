from django.db import models

class Product(models.Model):
    '''Продукт'''
    name = models.CharField(
        max_length=256,
        verbose_name='Название продукта'
    )
    product_type = models.CharField(
        max_length=128,
        verbose_name='Тип продукта',
        null=True,
        blank=True
    )
    category = models.CharField(
        max_length=128,
        verbose_name='Категория продукта',
        null=True,
        blank=True
    )
    image = models.ImageField(
        verbose_name='Изображение продукта',
        upload_to='products',
        null=True,
        blank=True
    )
    fix_price = models.FloatField(
        verbose_name='Фиксированная цена за кг продукта',
        null=True,
        blank=True
    )
    stock = models.IntegerField(
        verbose_name='Остаток продукта в кг',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self):
        return self.name
