# -*- encoding: utf-8 -*-
from django.db import models
from sincomplique.apps.principal.models import Municipio
from django.contrib.auth.models import User

class ProfileUser(models.Model):
	user = models.OneToOneField(User, primary_key = True)
	cc = models.CharField(max_length = 15)
	cc_residencia = models.ForeignKey(Municipio, related_name = "cc_residencia")
	telefono = models.CharField(max_length = 10)
	ciudad = models.ForeignKey(Municipio, related_name = "ciudad_residencia")

	def __str__(self):
		return str(self.user)