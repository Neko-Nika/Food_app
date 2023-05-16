from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import *

import os

class Command(BaseCommand):
    help = "Clear database"

    def clear(self,):
        print(len(Day.objects.all()))
        print(len(Meal.objects.all()))
            
    def handle(self, *args, **options):
        self.clear()
