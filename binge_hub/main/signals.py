from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from main.tasks import convert_480p
import os


"""
    Creates new `Video` object
"""
@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('video saved')
    if created:
        convert_480p(instance.video_file.path)
        print('video created')
      
  
"""
    Deletes file from filesystem when corresponding `Video` object is deleted.
"""
@receiver(post_delete, sender= Video)
def video_post_save(sender, instance, **kwargs):
    print('video delete')
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print('video deleted')