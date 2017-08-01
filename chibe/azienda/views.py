# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers

from .models import Partner

def azienda_index(request):
	return HttpResponse()

class azienda_login(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(azienda_login, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		imei = request.POST.get("imei", None)

		user = authenticate(request, username=imei, password=imei)

		if user is not None:
			login(request, user)
			return HttpResponse()
		else:
			return HttpResponse('Unauthorized', status=401)

class azienda_categorie(View):
	def dispatch(self, *args, **kwargs):
		return super(azienda_categorie, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):	
		user = request.user
		username = user.username
		#username = "868051020276493"
		partner = Partner.objects.get(username = username)
		
		categorie = partner.categorie.all()
		data = serializers.serialize('json', categorie, fields=('id', 'nome','id_immagine'))

		return HttpResponse(data)