__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.test import Client
from django.test import TestCase


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_renders_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'organizations/home.html')