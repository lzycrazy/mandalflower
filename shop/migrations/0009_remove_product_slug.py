# Generated by Django 3.2.5 on 2021-12-17 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]