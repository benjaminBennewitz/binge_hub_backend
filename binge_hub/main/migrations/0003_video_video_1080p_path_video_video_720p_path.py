# Generated by Django 5.0.6 on 2024-07-17 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_video_video_480p_path_alter_video_video_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_1080p_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_720p_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
