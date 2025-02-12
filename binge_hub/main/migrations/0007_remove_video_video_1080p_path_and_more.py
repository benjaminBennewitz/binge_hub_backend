# Generated by Django 5.0.6 on 2024-07-26 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_video_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='video_1080p_path',
        ),
        migrations.RemoveField(
            model_name='video',
            name='video_480p_path',
        ),
        migrations.RemoveField(
            model_name='video',
            name='video_720p_path',
        ),
        migrations.AddField(
            model_name='video',
            name='category',
            field=models.CharField(choices=[('new', 'New'), ('docu', 'Documentary'), ('drama', 'Drama'), ('romance', 'Romance')], default='new', max_length=50),
        ),
    ]
