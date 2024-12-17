import pandas as pd 
from django.core.management.base import BaseCommand  # Базовый класс для создания пользовательских команд Django
from catalog.models import Product  


class Command(BaseCommand):
    help = 'Импортируйте товары из файла CSV с удалением старых данных.'  # Описание команды, которое отображается при вызове help

    # Метод для добавления аргументов к команде
    def add_arguments(self, parser):
        # Добавляем обязательный аргумент: путь к CSV-файлу
        parser.add_argument('csv_file', type=str, help='CSV-файл, из которого можно загрузить данные.')

    # Основной метод, выполняющий логику команды
    def handle(self, *args, **kwargs):
        # Получаем путь к CSV-файлу из аргументов
        csv_file = kwargs['csv_file']

        # Читаем данные из CSV-файла в DataFrame
        # Используется разделитель `;`, так как это часто встречается в локализованных CSV-файлах
        df = pd.read_csv(csv_file, delimiter=';')

        # Удаление всех старых объектов из базы данных
        Product.objects.all().delete()  
        self.stdout.write(self.style.WARNING('Старые товары удалены из базы данных.'))

        # Импорт новых товаров из CSV
        for index, row in df.iterrows():  # Проходим по каждой строке DataFrame
            Product.objects.create(  # Создаем новый объект Product и сохраняем его в базе данных
                name=row['Название продукта'],  
                product_type=row['Тип продукта'],  
                category=row['Категория продукта'],  
                image=row['Изображение'],  
                fix_price=row['Фиксированная цена'],  
                stock=row['Остаток']  
            )

        
        self.stdout.write(self.style.SUCCESS('Успешно импортированы товары из CSV.'))


# Команда: python3 manage.py import_products data/Products.csv
