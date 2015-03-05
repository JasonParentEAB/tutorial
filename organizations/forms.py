__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django import forms

# Local imports...
from .models import Organization


class BootstrapMixin(object):
    def __init__(self, *args, **kwargs):
        super(BootstrapMixin, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control'
            })


class OrganizationForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Organization name'
            })
        }