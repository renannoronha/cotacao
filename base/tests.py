from django.test import TestCase
from django.urls import reverse, resolve

from .views import HomeView

# Create your tests here.
class TestUrls(TestCase):

    def test_home_url_resolves(self):
        self.assertEquals(resolve(reverse('home')).func.view_class, HomeView)