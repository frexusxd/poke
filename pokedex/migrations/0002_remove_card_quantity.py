# Generated by Django 5.0.7 on 2024-08-02 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='quantity',
        ),
    ]
