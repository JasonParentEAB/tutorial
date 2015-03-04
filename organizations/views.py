__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.shortcuts import render


def home_view(request):
    return render(request, 'organizations/home.html')