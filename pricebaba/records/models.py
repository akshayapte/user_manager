from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	mobile = models.IntegerField(max_length=10)
	age = models.IntegerField(max_length=2)
	date_of_birth = models.DateField()
	location = models.CharField(max_length=200)