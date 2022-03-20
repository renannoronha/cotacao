from django.test import TestCase, Client
from django.urls import reverse, resolve

from .views import HomeView

# Create your tests here.
class TestUrls(TestCase):

    def test_home_url_resolves(self):
        self.assertEquals(resolve(reverse('home')).func.view_class, HomeView)

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_get(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')