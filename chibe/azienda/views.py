# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers

from .models import Partner, Categoria, Acquisto, ContrattoMarketing
from main.models import Tribu, Utente

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
			#username = user.username
			username = "868051020276493"
			partner = Partner.objects.get(username = username)

			esistono_contratti = ContrattoMarketing.objects.filter(partners = partner).exists()
			if esistono_contratti:

				contratto = ContrattoMarketing.objects.get(partners = partner)
				is_valid_contract = contratto.is_valid()
				if is_valid_contract:
					login(request, user)
					return HttpResponse()
				else:
					return HttpResponse('Unauthorized', status=401)
			else:
				return HttpResponse('Unauthorized', status=401)
		else:
			return HttpResponse('Unauthorized', status=401)

class azienda_categorie(View):
	def dispatch(self, *args, **kwargs):
		return super(azienda_categorie, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):	
		#user = request.user
		#username = user.username
		username = "868051020276493"
		partner = Partner.objects.get(username = username)
		
		categorie = partner.categorie.all()
		data = serializers.serialize('json', categorie, fields=('id', 'nome','id_immagine'))

		return HttpResponse(data)

class azienda_search(View):
	def dispatch(self, *args, **kwargs):
		return super(azienda_search, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):	

		latitude = request.GET['latitude']
		longitude = request.GET['longitude']
		distanza = float(100)

		partners = Partner.objects_search.search(latitude, longitude, distanza)

		#data = serializers.serialize('json', partners, fields = ("distanza"))

		return JsonResponse(partners, safe = False)

class azienda_id(View):
	def dispatch(self, *args, **kwargs):
		return super(azienda_id, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):	

		su = Partner.objects.get(id = id)

		json_su = {
			"id" : su.id,
			"foto" : str(su.foto),
			"descrizione" : su.descrizione,
			"telefono" : su.telefono_fisso,
			"ragione_sociale" : su.ragione_sociale,
			"indirizzo" : su.indirizzo,
			"tribu_1" : su.tribu_1,
			"tribu_2" : su.tribu_2,
			"tribu_3" : su.tribu_3,
			"tribu_4" : su.tribu_4
		}

		return JsonResponse(json_su)


class azienda_pagamento(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(azienda_pagamento, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):	
		#user = request.user
		#username = user.username
		username = "868051020276493"
		partner = Partner.objects.get(username = username)

		categoria_id = request.POST['categoria_id']
		categoria = Categoria.objects.get(pk = categoria_id)

		codice = request.POST.get("code", None)
		utente_exists = Utente.objects.filter(codice = codice).exists()

		if not utente_exists:
			return HttpResponseNotFound("Codice non valido")
		else:
			utente = Utente.objects.get(codice = codice)

		importo = request.POST['importo']
		
		new_acquisto = Acquisto.objects.create(
			categoria = categoria,
			importo = importo,
			partner = partner,
			utente = utente
		)

		pp = calcolo_punti(partner, new_acquisto)

		utente_punti_vecchi = utente.punti
		utente.punti = utente_punti_vecchi + pp 
		utente.save()

		return HttpResponse()


def calcola_Mt(tribu_utente, tribu_partner):
	if tribu_utente is None or tribu_partner is None:
		return 0.5
	else:
		if tribu_partner == tribu_utente:
			return 0.75
		else:
			return 0.5

def calcolo_punti(partner, acquisto):
	utente = acquisto.utente
	tribu_utente = utente.tribu

	tribu_partner = partner.tribu

	contratto = ContrattoMarketing.objects.get(partners = partner)
	Pe = contratto.percentuale_marketing
	E = acquisto.importo
	Cp = 0.01

	Mt = calcola_Mt(tribu_utente, tribu_partner)

	Pp = ((E * Pe) * Mt) / Cp
	print "Punti piuma"
	print Pp
	return Pp




