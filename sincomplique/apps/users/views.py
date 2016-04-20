# -*- encoding: utf-8 -*-
from .forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.shortcuts import render, render_to_response

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import *
from .forms import PasswordResetRequestForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

class UserRegistrateView(FormView):
	template_name = 'users/registrate.html'
	form_class = RegistrateForm
	success_url = '/users/login'

	def get_context_data(self, **kwargs):
		context = super(UserRegistrateView, self).get_context_data(**kwargs)
		context['title'] = 'Registrate en sincomplique'
		return context

	def form_valid(self, form):
		form.registrate_user()
		return super(UserRegistrateView, self).form_valid(form)

class ResetPasswordRequestView(FormView):
	template_name = "users/password_reset_email.html"
	success_url = '/users/login'
	form_class = PasswordResetRequestForm

	@staticmethod
	def validate_email_address(email):
		try:
			validate_email(email)
			return True
		except ValidationError:
			return False

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			data= form.cleaned_data["email_or_username"]
		if self.validate_email_address(data) is True:
			associated_users= User.objects.filter(Q(email=data)|Q(username=data))
			if associated_users.exists():
				for user in associated_users:
					c = {
						'email': user.email,
						'domain': request.META['HTTP_HOST'],
						'site_name': 'SinComplique',
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'user': user,
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
					}
					subject_template_name = 'users/password_reset_subject.txt'
					email_template_name = 'users/password_reset_subject.html'
					subject = 'Cambio de Contraseña'
					subject = ''.join(subject.splitlines())
					email_txt = loader.render_to_string(subject_template_name, c)
					email_html = loader.render_to_string(email_template_name, c)
					send_mail(subject, email_html, settings.DEFAULT_FROM_EMAIL, [user.email])
				result = self.form_valid(form)
				messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
				return result
			result = self.form_invalid(form)
			messages.warning(request, 'No user is associated with this email address')
			return result
		else:
			associated_users= User.objects.filter(username=data)
			if associated_users.exists():
				for user in associated_users:
					c = {
						'email': user.email,
						'domain': request.META['HTTP_HOST'],
						'site_name': 'SinComplique',
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'user': user,
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
					}
					subject_template_name='users/password_reset_subject.txt'
					email_template_name='users/password_reset_subject.html'
					subject = loader.render_to_string(subject_template_name, c)
					subject = ''.join(subject.splitlines())
					email_txt = loader.render_to_string(subject_template_name, c)
					email_html = loader.render_to_string(email_template_name, c)
					send_mail(subject, email_html, settings.DEFAULT_FROM_EMAIL , [user.email])
				result = self.form_valid(form)
				messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
				return result
			result = self.form_invalid(form)
			messages.error(request, 'This username does not exist in the system.')
			return result
		messages.error(request, 'Invalid Input')
		return self.form_invalid(form)

class PasswordResetConfirmView(FormView):
	template_name = "users/password_reset_email.html"
	success_url = '/users/login'
	form_class = SetPasswordForm

	def post(self, request, uidb64=None, token=None, *arg, **kwargs):
		UserModel = get_user_model()
		form = self.form_class(request.POST)
		assert uidb64 is not None and token is not None  # checked by URLconf
		try:
			uid = urlsafe_base64_decode(uidb64)
			user = UserModel._default_manager.get(pk=uid)
		except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
			user = None

		if user is not None and default_token_generator.check_token(user, token):
			if form.is_valid():
				new_password= form.cleaned_data['new_password2']
				user.set_password(new_password)
				user.save()
				messages.success(request, 'Password has been reset.')
				return self.form_valid(form)
			else:
				messages.error(request, 'Password reset has not been unsuccessful.')
				return self.form_invalid(form)
		else:
			messages.error(request,'The reset password link is no longer valid.')
			return self.form_invalid(form)