__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Third-party imports...
from mock import patch

# Django imports...
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase

# Local imports...
from ..forms import OrganizationForm
from ..models import Organization
from ..views import create_view


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_renders_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'organizations/home.html')

    def test_view_returns_organization_list(self):
        organization = Organization.objects.create(name='test')
        response = self.client.get('/')
        self.assertListEqual(response.context['organizations'], [organization])


class CreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_view_renders_template(self):
        response = self.client.get('/create/')
        self.assertTemplateUsed(response, 'organizations/create.html')

    def test_view_redirects_home_on_post(self):
        response = self.client.post('/create/')
        self.assertRedirects(response, '/')

    def test_view_creates_organization_on_post(self):
        self.client.post('/create/', data={'name': 'test'})
        self.assertEqual(Organization.objects.count(), 1)
        organization = Organization.objects.last()
        self.assertEqual(organization.name, 'test')

    def test_create_view_returns_organization_form(self):
        response = self.client.get('/create/')
        self.assertIsInstance(response.context['form'], OrganizationForm)

    @patch('organizations.views.OrganizationForm')
    def test_passes_post_data_to_form(self, mock_organization_form):
        request = self.factory.post('/create/', data={'name': 'test'})
        create_view(request)
        mock_organization_form.assert_any_call(data=request.POST)

    @patch('organizations.views.OrganizationForm')
    def test_saves_organization_for_valid_data(self, mock_organization_form):
        mock_form = mock_organization_form.return_value
        mock_form.is_valid.return_value = True
        mock_form.save.return_value = None
        request = self.factory.post('/create/', data={'name': 'test'})
        create_view(request)
        self.assertTrue(mock_form.save.called)