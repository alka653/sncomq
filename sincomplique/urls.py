from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('sincomplique.apps.principal.urls')),
	url(r'^users/', include('sincomplique.apps.users.urls')),
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]
