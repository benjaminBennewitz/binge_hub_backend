from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from main.tasks import convert_480p, convert_720p, convert_1080p
from django.conf import settings
import os
import django_rq


"""
    Creates new `Video` object
"""
@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        # Convert videos and update paths
        source_path = instance.video_file.path

        # Get the base name of the video file without the extension
        base_name = os.path.splitext(os.path.basename(source_path))[0]

        # Create paths for the converted videos in the same directory as the source video
        video_dir = os.path.dirname(source_path)
        instance.video_480p_path = os.path.join('video', base_name + '_480p.mp4')
        instance.video_720p_path = os.path.join('video', base_name + '_720p.mp4')
        instance.video_1080p_path = os.path.join('video', base_name + '_1080p.mp4')

        # Save the instance with updated paths
        instance.save()

        # Queue
        queue = django_rq.get_queue('default')
        queue.enqueue(convert_480p, source_path, os.path.join(video_dir, base_name + '_480p.mp4'))
        queue.enqueue(convert_720p, source_path, os.path.join(video_dir, base_name + '_720p.mp4'))
        queue.enqueue(convert_1080p, source_path, os.path.join(video_dir, base_name + '_1080p.mp4'))
      
  
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
    def delete_file(file_path):
        if file_path:
            # Convert relative path to absolute path
            absolute_path = os.path.join(settings.MEDIA_ROOT, file_path)
            if os.path.isfile(absolute_path):
                os.remove(absolute_path)
                print(f'{file_path} deleted')

    # Delete converted video files
    delete_file(instance.video_480p_path)
    delete_file(instance.video_720p_path)
    delete_file(instance.video_1080p_path)