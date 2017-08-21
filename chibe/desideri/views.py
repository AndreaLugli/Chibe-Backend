# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from .models import Desiderio
from main.models import Gruppo, Utente

def desideri_home(request):

	#data_inizio
	#data_fine

	desideri = Desiderio.objects.all().values("id", "nome", "descrizione_breve", "in_evidenza", "num_gruppo")

	return JsonResponse(list(desideri), safe = False)

class desideri_id(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(desideri_id, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):
		d = Desiderio.objects.get(pk = id)

		desiderio_json = {
			"id" : d.id,
			"nome" : d.nome,
			"descrizione_lunga" : d.descrizione_lunga,
			"immagine" : d.immagine,
			"num_gruppo" : d.num_gruppo
		}

		return JsonResponse(desiderio_json, safe = False)

	def post(self, request, id, *args, **kwargs):
		#user = request.user
		#username = user.username
		username = "bella"
		utente = Utente.objects.get(username = username)		

		d = Desiderio.objects.get(pk = id)

		gr, created = Gruppo.objects.get_or_create(desiderio = d, utente_admin = utente)
		
		if created:
			gr.utenti.add(utente)

		return HttpResponse()

