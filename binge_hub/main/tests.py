from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Video
from .views import VideoListView
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.views import LoginView as DjangoLoginView
import subprocess
import time
import redis
from django.test import TestCase

class RedisTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Start Redis server
        cls.redis_process = subprocess.Popen(['redis-server'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)  # Wait a moment for Redis to start

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Stop Redis server
        cls.redis_process.terminate()
        cls.redis_process.wait()

    def test_something(self):
        r = redis.Redis()
        r.set('foo', 'bar')
        value = r.get('foo')
        self.assertEqual(value, b'bar')


# Model tests
class VideoModelTest(TestCase):
    def setUp(self):
        # Setting up initial data for tests
        Video.objects.create(
            title="Test Video",
            description="Test Description",
            category="docu",
            video_file=SimpleUploadedFile("test_video.mp4", b"file_content")
        )

    def test_video_creation(self):
        """
        Test if the video is created successfully.
        """
        video = Video.objects.get(title="Test Video")
        self.assertEqual(video.description, "Test Description")
        self.assertEqual(video.category, "docu")
        self.assertEqual(str(video), video.title)

    def test_default_is_new(self):
        """
        Test the default value of is_new field.
        """
        video = Video.objects.get(title="Test Video")
        self.assertFalse(video.is_new)

    def test_default_created_at(self):
        """
        Test the default value of created_at field.
        """
        video = Video.objects.get(title="Test Video")
        self.assertEqual(video.created_at, date.today())

# View tests
class VideoListViewTest(APITestCase):
    def setUp(self):
        # Setting up initial data and client for tests
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.video = Video.objects.create(
            title="Test Video",
            description="Test Description",
            category="docu",
            video_file=SimpleUploadedFile("test_video.mp4", b"file_content")
        )

    def test_video_list_view_authenticated(self):
        """
        Ensure the video list view works for authenticated users.
        """
        self.client.login(username='testuser', password='testpassword')
        url = reverse('video-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Video")

    def test_video_list_view_unauthenticated(self):
        """
        Ensure the video list view requires authentication.
        """
        url = reverse('video-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# URL resolution tests
class UrlsTest(TestCase):
    def test_video_list_url(self):
        """
        Test if the video list URL is resolved correctly.
        """
        url = reverse('video-list')
        self.assertEqual(resolve(url).func.view_class, VideoListView)

    def test_login_url(self):
        """
        Test if the login URL is resolved correctly.
        """
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, DjangoLoginView)