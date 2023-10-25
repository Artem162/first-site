# Generated by Django 5.0a1 on 2023-10-11 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_category_movie_cat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Категорія', 'verbose_name_plural': 'Категорії'},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['time_create', 'title'], 'verbose_name': 'Кращі кінофільми', 'verbose_name_plural': 'Кращі кінофільми'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Категорія'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='movies.category', verbose_name='Категорія'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='content',
            field=models.TextField(blank=True, verbose_name='Текст статты'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Опубліковано?'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='photo',
            field=models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='фото'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата створення'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='даа останнього оновлення'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
    ]
