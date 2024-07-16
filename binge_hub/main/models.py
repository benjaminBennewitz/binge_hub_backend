from datetime import date
from django.db import models

class Video(models.Model):
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='video', blank=True, null=True)
    video_480p_path = models.CharField(max_length=255, blank=True, null=True)  # Neues Feld hinzufügen

    def __str__(self):
        return self.title
