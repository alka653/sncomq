# -*- encoding: utf-8 -*-
from django.db import models

class Departamento(models.Model):
	desc = models.CharField(max_length = 45)

	def __str__(self):
		return self.desc

	def __unicode__(self):
		return self.desc

class Municipio(models.Model):
	depto = models.ForeignKey(Departamento)
	desc = models.CharField(max_length = 45)

	def __str__(self):
		return self.desc

	def __unicode__(self):
		return self.desc