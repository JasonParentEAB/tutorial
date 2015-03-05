__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django import forms

# Local imports...
from .models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Organization name'
            })
        }