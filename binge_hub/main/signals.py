from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from main.tasks import convert_480p, convert_720p, convert_1080p
import os


"""
    Creates new `Video` object
"""
@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        # Convert videos and update paths
        source_path = instance.video_file.path
        instance.video_480p_path = source_path + '_480p.mp4'
        instance.video_720p_path = source_path + '_720p.mp4'
        instance.video_1080p_path = source_path + '_1080p.mp4'

        # Save the instance with updated paths
        instance.save()

        # Run conversion tasks synchronously
        convert_480p(source_path)
        convert_720p(source_path)
        convert_1080p(source_path)
      
  
"""
    Deletes main Video and the converted videos.
"""
@receiver(post_delete, sender=Video)
def delete_video_files(sender, instance, **kwargs):
    print('video delete')
    # Delete original video file
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            print('original video deleted')

    # Delete converted video files
    if instance.video_480p_path:
        if os.path.isfile(instance.video_480p_path):
            os.remove(instance.video_480p_path)
            print('480p video deleted')

    if instance.video_720p_path:
        if os.path.isfile(instance.video_720p_path):
            os.remove(instance.video_720p_path)
            print('720p video deleted')

    if instance.video_1080p_path:
        if os.path.isfile(instance.video_1080p_path):
            os.remove(instance.video_1080p_path)
            print('1080p video deleted')