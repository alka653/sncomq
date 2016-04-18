# -*- encoding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import json

def download_file(request):
	name_file = request.GET.get('file')
	file_docx = open('sincomplique/static/files/'+name_file, 'r')
	response = HttpResponse()
	response['Content-Disposition'] = 'attachment; filename='+name_file
	response['Content-Encoding'] = 'UTF-8'
	response['Content-type'] = 'text/html; charset=UTF-8'
	response.write(file_docx.read())
	file_docx.close()
	return response

@csrf_exempt
def get_municipio(request):
	results = []
	response = {}
	for depto in Departamento.objects.get(pk = request.POST.get('depto')).municipio_set.all():
		response['pk'] = depto.pk
		response['muni'] = depto.desc.encode('utf8')
		results.append(response)
		response = {}
	return HttpResponse(json.dumps(results), content_type = 'application/json')