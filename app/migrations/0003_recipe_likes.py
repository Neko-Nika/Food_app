# Generated by Django 4.1.7 on 2023-04-29 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_step_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]