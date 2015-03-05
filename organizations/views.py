__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render

# Local imports...
from .forms import OrganizationForm
from .models import Organization


def home_view(request):
    return render(request, 'organizations/home.html', {
        'organizations': list(Organization.objects.all())
    })


def create_view(request):
    form = OrganizationForm()

    if request.method == 'POST':
        form = OrganizationForm(data=request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('home'))

    return render(request, 'organizations/create.html', {
        'form': form
    })