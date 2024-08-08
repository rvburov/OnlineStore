import pandas as pd
from django.core.management.base import BaseCommand
from catalog.models import Product

class Command(BaseCommand):
    help = 'Импортируйте товары из файла CSV.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV-файл, из которого можно загрузить данные.')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        df = pd.read_csv(csv_file, delimiter=';')

        for index, row in df.iterrows():
            product = Product(
                name=row['Название продукта'],
                image=row['Изображение'],
                category=row['Категория'],
                fix_price=row['Фиксированная цена'],
                stock=row['Остаток']
            )
            product.save()
        
        self.stdout.write(self.style.SUCCESS('Успешно импортированы товары из CSV.'))

# python3 manage.py import_products data/Products.csv
