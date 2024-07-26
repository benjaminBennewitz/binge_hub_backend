# Generated by Django 5.0.6 on 2024-07-26 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_video_is_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.CharField(choices=[('crime', 'Crime'), ('docu', 'Documentary'), ('drama', 'Drama'), ('romance', 'Romance')], default='new', max_length=50),
        ),
    ]