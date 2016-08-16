from __future__ import unicode_literals

from django.db import models

# Create your models here.
class generic_register(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __first_name__(self):
		return self.first_name

	def __last_name__(self):
		return self.last_name

	def __email__(self):
		return self.email