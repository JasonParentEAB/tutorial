__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=250)