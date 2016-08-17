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

class company(models.Model):
	organization_name = models.CharField(max_length=200)
	organization_type = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	neighborhood = models.CharField(max_length=200)
	adress = models.CharField(max_length=200)
	cnpj = models.CharField(max_length=200)
	latitude = models.DecimalField(max_digits=9, decimal_places=7)
	longitude = models.DecimalField(max_digits=9, decimal_places=7)
	is_active = models.IntegerField(default=1)
	description = models.CharField(max_length=400)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __organization_name__(self):
		return self.organization_name

	def __organization_type__(self):
		return self.organization_type

	def __phone__(self):
		return self.phone

	def __email__(self):
		return self.email

	def __city__(self):
		return self.city

	def __state__(self):
		return self.state

	def __neighborhood__(self):
		return self.neighborhood

	def __adress__(self):
		return self.adress

	def __cnpj__(self):
		return self.cnpj

	def __latitude__(self):
		return self.latitude

	def __longitude__(self):
		return self.longitude

	def __is_active__(self):
		return self.is_active

	def __description__(self):
		return self.description

	def __created_at__(self):
		return self.created_at

class residue(models.Model):
	residue_name = models.CharField(max_length=200)
	unity = models.CharField(max_length=200)

	def __residue_name__(self):
		return self.residue_name

	def __unity__(self):
		return self.unity

class receptivity(models.Model):
	residue_id = models.IntegerField(default=0)
	company_id = models.IntegerField(default=0)
	minimun = models.IntegerField(default=0)
	maximun = models.IntegerField(default=0)
	is_active = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __residue_id__(self):
		return self.residue_id

	def __company_id__(self):
		return self.company_id

	def __minimun__(self):
		return self.minimun

	def __maximun__(self):
		return self.maximun

	def __is_active__(self):
		return self.is_active

	def __created_at__(self):
		return self.created_at

class member(models.Model):
	email = models.CharField(max_length=200)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __first_name__(self):
		return self.first_name

	def __last_name__(self):
		return self.last_name

	def __email__(self):
		return self.email

	def __phone__(self):
		return self.phone

	def __created_at__(self):
		return self.created_at

class search_history(models.Model):
	text = models.CharField(max_length=200)
	member_id = models.IntegerField(default=0)
	latitude = models.DecimalField(max_digits=9, decimal_places=7)
	longitude = models.DecimalField(max_digits=9, decimal_places=7)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __text__(self):
		return self.text

	def __member_id__(self):
		return self.member_id

	def __latitude__(self):
		return self.latitude

	def __longitude__(self):
		return self.longitude

	def __created_at__(self):
		return self.created_at