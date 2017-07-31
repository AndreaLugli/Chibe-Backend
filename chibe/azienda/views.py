# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Esercente

def azienda_index(request):
	return HttpResponse()

class azienda_login(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(azienda_login, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		imei = request.POST.get("imei", None)

		user = authenticate(request, username=imei, password=imei)

		print user

		if user is not None:
			login(request, user)
			return HttpResponse()
		else:
			return HttpResponse('Unauthorized', status=401)
