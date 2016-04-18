from .views import *
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = patterns('sincomplique.apps.users.views',
	url(r'^registrate/$', login_forbidden(UserRegistrateView.as_view()), name = 'registrate'),
)

urlpatterns += [
	url(r'^login/$', login_forbidden(auth_views.login), {'template_name': 'users/login.html', 'extra_context': {'title': 'Ingreso'}}, name = 'login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/users/login'}, name = 'logout')
]