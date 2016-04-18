# -*- encoding: utf-8 -*-
from .forms import *
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

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