# Generated by Django 5.0.6 on 2024-12-17 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Имя')),
                ('phone', models.CharField(blank=True, max_length=16, null=True, verbose_name='Телефон')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='Адрес')),
                ('check_list', models.BooleanField(blank=True, null=True, verbose_name='Согласие на обработку персональных данных')),
                ('time', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время доставки')),
                ('status', models.CharField(choices=[('waiting', 'Ожидание доставки'), ('delivered', 'Доставлено')], default='waiting', max_length=10, verbose_name='Статус заказа')),
                ('delivery_price', models.FloatField(default=0, verbose_name='Цена за доставку')),
                ('total_price', models.FloatField(default=0, verbose_name='Итоговая цена')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=256, null=True, verbose_name='Название продукта')),
                ('product_weight', models.FloatField(default=0, verbose_name='Вес продукта')),
                ('product_price', models.FloatField(default=0, verbose_name='Цена продукта')),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение продукта')),
            ],
            options={
                'verbose_name': 'Корзина заказа',
                'verbose_name_plural': 'Корзина заказов',
            },
        ),
    ]
