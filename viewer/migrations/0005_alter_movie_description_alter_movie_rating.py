# Generated by Django 4.1.1 on 2024-05-22 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0004_alter_genre_name_alter_movie_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
