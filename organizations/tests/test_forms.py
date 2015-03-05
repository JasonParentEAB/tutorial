__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.test import TestCase

# Local imports...
from ..forms import OrganizationForm


class OrganizationFormTest(TestCase):
    def test_form_has_required_fields(self):
        form = OrganizationForm()
        self.assertIn('id="id_name"', form.as_p())