# Generated by Django 4.1.7 on 2023-05-04 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='weight',
            field=models.FloatField(default=0),
        ),
    ]
