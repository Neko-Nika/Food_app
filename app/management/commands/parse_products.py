from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import *

import pandas as pd
import requests
from bs4 import BeautifulSoup

import os

URL = 'https://calorizator.ru/product/all'
PAGES_TO_PARSE = 81
DESTINATION = 'app/static/files/products.csv'


class Command(BaseCommand):
    help = "Parses products from URL into .csv file and fills database"

    def parse(self):
        """Parses data."""
        
        df = pd.DataFrame(columns=['product', 'proteins', 'fats', 'carbohydrates', 'calories'])

        for i in range(PAGES_TO_PARSE):
            response = requests.get(URL + f'?page={i}')
            bs = BeautifulSoup(response.text, 'lxml')
            
            page = dict(product=[], proteins=[], fats=[], carbohydrates=[], calories=[])
            products = bs.find('table', {'class': 'views-table'}).find('tbody').find_all('tr')
            for product in products:
                name = product.find("td", {'class': 'views-field-title'}).find("a").text.strip()
                proteins = product.find("td", {'class': 'views-field-field-protein-value'}).text.strip()
                fats = product.find("td", {'class': 'views-field-field-fat-value'}).text.strip()
                carbohydrates = product.find("td", {'class': 'views-field-field-carbohydrate-value'}).text.strip()
                calories = product.find("td", {'class': 'views-field-field-kcal-value'}).text.strip()

                if name == "" or proteins == "" or fats == "" or carbohydrates == "" or calories == "":
                    continue

                page['product'].append(name)
                page['proteins'].append(float(proteins))
                page['fats'].append(float(fats))
                page['carbohydrates'].append(float(carbohydrates))
                page['calories'].append(int(calories))

            df = pd.concat([df, pd.DataFrame(page)], ignore_index=True)

        df.to_csv(DESTINATION, sep=',', index=False)
    
    def fill(self):
        """Fills database with products."""

        df = pd.read_csv(DESTINATION, sep=',')
        for _, row in df.iterrows():
            product = Product.objects.create(
                name=row['product'],
                proteins=row['proteins'],
                fats=row['fats'],
                carbohydrates=row['carbohydrates'],
                calories=row['calories']
            )
            product.save()
            
    def handle(self, *args, **options):
        if os.path.exists('app/static/files/products.csv') is False:
            self.parse()

        self.fill()
