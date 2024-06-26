# Generated by Django 4.1.1 on 2024-05-28 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0006_alter_genre_options_alter_movie_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='length',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='title_cz',
            field=models.CharField(max_length=185, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='movies', to='viewer.genre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='countries',
            field=models.ManyToManyField(blank=True, related_name='movies', to='viewer.country'),
        ),
    ]
