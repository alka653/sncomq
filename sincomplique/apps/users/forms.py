# -*- encoding: utf-8 -*-
from sincomplique.apps.principal.models import *
from django.forms import *
from django import forms
from .models import *

class PasswordResetRequestForm(forms.Form):
	email_or_username = forms.CharField(label = 'Usuario o Contraseña', widget = forms.EmailInput(attrs = {'class': 'form-control', 'required': True}))

class SetPasswordForm(forms.Form):
	error_messages = {
		'password_mismatch': ("The two password fields didn't match."),
	}
	new_password1 = forms.CharField(label=("New password"), widget=forms.PasswordInput)
	new_password2 = forms.CharField(label=("New password confirmation"), widget=forms.PasswordInput)

	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if password1 and password2:
			if password1 != password2:
				raise forms.ValidationError(
					self.error_messages['password_mismatch'],
					code='password_mismatch',
				)
		return password2

class RegistrateForm(forms.Form):
	email = forms.EmailField(label = 'Correo electrónico', widget = forms.EmailInput(attrs = {'class': 'form-control', 'required': True}))
	password = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(attrs = {'class': 'form-control', 'required': True}))
	first_name = forms.CharField(label = 'Nombres', widget = TextInput(attrs = {'class': 'form-control', 'maxlength': '30', 'required': True}))
	last_name = forms.CharField(label = 'Apellidos', widget = TextInput(attrs = {'class': 'form-control', 'maxlength': '30', 'required': True}))
	telefono = forms.CharField(label = 'Número celular', widget = TextInput(attrs = {'class': 'number form-control number', 'maxlength': '10', 'required': False}))
	cc = forms.CharField(label = 'Número de cédula', widget = TextInput(attrs = {'class': 'number form-control number', 'maxlength': '10', 'required': False}))
	cc_residencia_depart = forms.ModelChoiceField(label = 'Departamento de expedición', queryset = Departamento.objects.all(), widget = forms.Select(attrs = {'class': 'form-control', 'required': True}))
	cc_residencia_muni = forms.CharField(label = 'Municipio de expedición', widget = Select(attrs = {'class': 'form-control', 'required': True}))
	ciudad_residencia_depart = forms.ModelChoiceField(label = 'Departamento de residencia', queryset = Departamento.objects.all(), widget = forms.Select(attrs = {'class': 'form-control', 'required': True}))
	ciudad_residencia_muni = forms.CharField(label = 'Ciudad de residencia', widget = Select(attrs = {'class': 'form-control', 'required': True}))

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email = email, username = email).exists():
			raise forms.ValidationError('El email ya se ecuentra en uso.')
		return email

	def registrate_user(self):
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		username = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		email = self.cleaned_data.get('email')
		telefono = self.cleaned_data.get('telefono')
		cc = self.cleaned_data.get('cc')
		cc_residencia_muni = Municipio.objects.get(pk = self.cleaned_data.get('cc_residencia_muni'))
		ciudad_residencia_muni = Municipio.objects.get(pk = self.cleaned_data.get('ciudad_residencia_muni'))
		user = User.objects.create_user(username, email, password)
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		profile = ProfileUser(user = user,cc = cc, telefono = telefono, cc_residencia = cc_residencia_muni, ciudad = ciudad_residencia_muni)
		profile.save()