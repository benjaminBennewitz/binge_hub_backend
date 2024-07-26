from datetime import date
from django.db import models

class Video(models.Model):
    CATEGORY_CHOICES = [
        ('crime', 'Crime'),
        ('docu', 'Documentary'),
        ('drama', 'Drama'),
        ('romance', 'Romance'),
    ]
     
    is_new = models.BooleanField(default=False)    
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='new')
    video_file = models.FileField(upload_to='video', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='video/thumbs', blank=True, null=True)
    video_480p_path = models.CharField(max_length=255, blank=True, null=True)
    video_720p_path = models.CharField(max_length=255, blank=True, null=True)
    video_1080p_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title