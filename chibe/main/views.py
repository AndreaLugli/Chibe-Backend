# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers
from random import randint
from .models import Utente, OnBoard
from .models import Provincia, Scuola

def check_connected(request):
	if request.user.is_authenticated():
		
		username = request.user.username
		utente = Utente.objects.get(username = username)
		onboard = OnBoard.objects.get(utente = utente)

		complete = onboard.complete
		step_1 = onboard.step_1
		step_2 = onboard.step_2
		step_3 = onboard.step_3

		if complete:
			output = 0
		elif not step_1:
			output = 1
		elif not step_2:
			output = 2
		elif not step_3:
			output = 3

		return HttpResponse(output)
	else:
		return HttpResponse('Unauthorized', status=401)

class utente_login(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(utente_login, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		username = request.POST.get("username", None)
		password = request.POST.get("password", None)

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			utente = Utente.objects.get(username = username)
			onboard = OnBoard.objects.get(utente = utente)

			complete = onboard.complete
			step_1 = onboard.step_1
			step_2 = onboard.step_2
			step_3 = onboard.step_3

			if complete:
				output = 0
			elif not step_1:
				output = 1
			elif not step_2:
				output = 2
			elif not step_3:
				output = 3

			return HttpResponse(output)
		else:
			return HttpResponse('Unauthorized', status=401)

class utente_register(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(utente_register, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		username = request.POST.get("username", None)
		email = request.POST.get("email", None)

		email = email.strip()
		username = username.strip()
		email = email.lower()

		username_ex = Utente.objects.filter(username = username).exists()
		if username_ex:
			return HttpResponseBadRequest("Username già in uso")

		email_ex = Utente.objects.filter(email = email).exists()
		if email_ex:
			return HttpResponseBadRequest("Email già in uso")


		password_1 = request.POST.get("password_1", None)
		password_2 = request.POST.get("password_2", None)

		if password_1 != password_2:
			return HttpResponseBadRequest("Le due password non coincidono")


		codice = generate_code()

		utente_obj = Utente.objects.create_user(
			username = username,
			email = email,
			password = password_1,
			codice = codice
		)

		OnBoard.objects.create(utente = utente_obj)

		user = authenticate(request, username=username, password=password_1)

		if user is not None:
			login(request, user)		

		return HttpResponse()

def generate_code():
	code = randint(100000000, 999999999)

	while Utente.objects.filter(codice = str(code)).exists():
		code = randint(100000000, 999999999)

	return code 

class utente_step1(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(utente_step1, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		#user = request.user
		#username = user.username
		username = "bella"
		utente = Utente.objects.get(username = username)

		nome = request.POST['nome']
		cognome = request.POST['cognome']
		cellulare = request.POST['cellulare']

		utente.first_name = nome
		utente.last_name = cognome
		utente.telefono_cellulare = cellulare
		utente.save()

		onboard_obj = OnBoard.objects.get(utente = utente)
		onboard_obj.step_1 = True
		onboard_obj.save()

		return HttpResponse()

class utente_step2(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(utente_step2, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		#user = request.user
		#username = user.username
		username = "bella"
		utente = Utente.objects.get(username = username)

		#Gestione avatar

		onboard_obj = OnBoard.objects.get(utente = utente)
		onboard_obj.step_2 = True
		onboard_obj.save()

		return HttpResponse()

class utente_province(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(utente_province, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):

		province = Provincia.objects.filter(attivo = True)
		data = serializers.serialize('json', province, fields=('id', 'nome', 'codice'))

		return HttpResponse(data)

class utente_province_id(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(utente_province_id, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):

		provincia = Provincia.objects.get(pk = id)

		scuole = Scuola.objects.filter(provincia = provincia)
		data = serializers.serialize('json', scuole, fields=('id', 'nome'))

		return HttpResponse(data)

class utente_step3(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(utente_step3, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		#user = request.user
		#username = user.username
		username = "bella"
		utente = Utente.objects.get(username = username)

		provincia_id = request.POST['provincia_id']
		provincia = Provincia.objects.get(pk = provincia_id)

		scuola_id = request.POST['scuola_id']
		scuola = Scuola.objects.get(pk = scuola_id)

		classe = request.POST.get("classe", None)
		newsletter = request.POST.get("newsletter", None)

		utente.classe = classe
		utente.provincia = provincia
		utente.scuola = scuola
		utente.save()

		onboard_obj = OnBoard.objects.get(utente = utente)
		onboard_obj.step_3 = True
		onboard_obj.complete = True
		onboard_obj.save()

		return HttpResponse()
