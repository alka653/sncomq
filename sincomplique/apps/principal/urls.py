from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('sincomplique.apps.principal.views',
	url(r'^$', TemplateView.as_view(template_name = 'home/index.html'), {'title': 'Bienvenido'}, name = 'home'),
	url(r'^get-municipio/$', 'get_municipio', name = 'get_municipio'),
	url(r'^download-file/$', 'download_file', name = 'download_file'),
)