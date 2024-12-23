# Generated by Django 4.2.17 on 2024-12-23 20:16

import book.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_rename_stock_count_bookedition_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedition',
            name='format',
            field=models.CharField(choices=[['Hardcover', 'Hardcover'], ['Paperback', 'Paperback'], ['eBook', 'Ebook'], ['Other', 'Other']], default=book.models.FormatEnum['OTHER'], max_length=50),
        ),
        migrations.AlterField(
            model_name='bookedition',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
