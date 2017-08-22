# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers
from datetime import datetime
from random import randint
from .models import Utente, OnBoard, Tribu
from .models import Provincia, Scuola
from .models import Gruppo
from django.conf import settings
import StringIO
from PIL import Image
from django.db.models import Q
import hashlib

AVATAR_MEDIA_ROOT = settings.MEDIA_ROOT + "/avatar"

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
		avatar = request.POST.get("avatar", None)
		utente.avatar = avatar
		utente.save()

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

@csrf_exempt
def upload_picture(request):

	f = request.FILES['file']

	str = ""
	for c in f.chunks():
		str += c
	imagefile  = StringIO.StringIO(str)
	image = Image.open(imagefile)

	now = datetime.now()
	now_formatted = now.strftime("%Y-%m-%d_%H-%M")
	token = hashlib.sha224(now_formatted).hexdigest()	
	outfile = AVATAR_MEDIA_ROOT + '/' + token + '.jpg'
	image.save(outfile, "JPEG")	

	output = "/media/avatar/" + token + '.jpg'

	return HttpResponse(output)

def get_code(request):
	#user = request.user
	#username = user.username
	username = "bella"
	utente = Utente.objects.get(username = username)
	codice = utente.codice
	return HttpResponse(codice)

def search_amico(request):
	#user = request.user
	#username = user.username
	username = "bella"
	utente = Utente.objects.get(username = username)

	amico = request.GET.get("amico", None)

	amici = utente.amici.filter().values_list("id", flat = True)

	utenti = Utente.objects.filter(
		Q(email__icontains=amico) |
		Q(first_name__icontains=amico) |
		Q(last_name__icontains=amico) |
		Q(username__icontains=amico) |
		Q(telefono_cellulare__icontains=amico) |
		Q(codice__icontains=amico)
	).exclude(username = username).exclude(pk__in=amici).values("username", "id", "first_name", "last_name")

	return JsonResponse(list(utenti), safe = False)

def utente_amici(request):
	#user = request.user
	#username = user.username
	username = "bella"
	utente = Utente.objects.get(username = username)

	amici = utente.amici.all().values("username", "id", "first_name", "last_name")

	return JsonResponse(list(amici), safe = False)

@csrf_exempt
def utente_amico_add(request):
	#user = request.user
	#username = user.username
	username = "bella"
	utente = Utente.objects.get(username = username)

	id_amico = request.POST['id_amico']
	amico = Utente.objects.get(pk = id_amico)

	utente.amici.add(amico)

	return HttpResponse()

@csrf_exempt
def utente_amico_delete(request):
	#user = request.user
	#username = user.username
	username = "bella"
	utente = Utente.objects.get(username = username)

	id_amico = request.POST['id_amico']
	amico = Utente.objects.get(pk = id_amico)

	utente.amici.remove(amico)

	return HttpResponse()

@csrf_exempt
def utente_info(request):
	#user = request.user
	#username = user.username
	username = "bella"
	utente = Utente.objects.get(username = username)

	modifica_tribu = None

	tribu_timestamp = utente.tribu_timestamp
	if tribu_timestamp:
		now = datetime.now().date()
		diff = now - tribu_timestamp
		days = diff.days
		if days >= 60:
			modifica_tribu = True

	json_utente = {
		"id" : utente.id,
		"avatar" : utente.avatar,
		"username" : utente.username,
		"descrizione" : utente.descrizione,
		"nome" : utente.first_name,
		"cognome" : utente.last_name,
		"punti" : utente.punti,
		"tribu" : utente.tribu.nome,
		"modifica_tribu" : modifica_tribu
	}

	return JsonResponse(json_utente)	

@csrf_exempt
def utente_tribu(request):
	#user = request.user
	#username = user.username
	username = "bella"
	utente = Utente.objects.get(username = username)

	tribu = request.POST['tribu']

	#orsi
	#aquile
	#lupi
	#puma
	#volpi

	tribu_obj = Tribu.objects.get(nome__iexact = tribu)
	tribu_timestamp = datetime.now().date()

	utente.tribu = tribu_obj
	utente.tribu_timestamp = tribu_timestamp
	utente.save()

	return HttpResponse()

@csrf_exempt
def utente_modifica(request):
	#user = request.user
	#username = user.username
	username = "bella"
	utente = Utente.objects.get(username = username)

	descrizione = request.POST['descrizione']

	utente.descrizione = descrizione
	utente.save()


	return HttpResponse()

@csrf_exempt
def utente_desideri(request):
	#user = request.user
	#username = user.username
	username = "bella"
	utente = Utente.objects.get(username = username)

	gruppi = Gruppo.objects.filter(utenti = utente).values("punti", "desiderio__nome", "id")

	return JsonResponse(list(gruppi), safe = False)

def utente_punti(request):
	#user = request.user
	#username = user.username
	username = "bella"
	utente = Utente.objects.get(username = username)
	punti = utente.punti

	return HttpResponse(punti)	

@csrf_exempt
def utente_inviapunti(request):
	#user = request.user
	#username = user.username
	username = "bella"
	utente = Utente.objects.get(username = username)

	amico_id = request.POST['amico_id']
	amico = Utente.objects.get(pk = amico_id)

	punti = request.POST['punti']
	punti = int(punti)

	utente_punti_old = utente.punti
	utente_punti_new = utente_punti_old - punti
	utente.punti = utente_punti_new
	utente.save()

	amico_punti_old = amico.punti
	amico_punti_new = amico_punti_old + punti
	amico.punti = amico_punti_new
	amico.save()

	return HttpResponse()




