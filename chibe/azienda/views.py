# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers
from chibe.push import notifica_pagamento

from azienda.models import Partner, Categoria, Acquisto, ContrattoMarketing
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
			username = user.username
			#username = "868051020276493"
			partner = Partner.objects.get(username = username)

			attivo = partner.attivo
			if attivo:
				esistono_contratti = ContrattoMarketing.objects.filter(partners = partner).exists()
				if esistono_contratti:

					contratto = ContrattoMarketing.objects.get(partners = partner)
					is_valid_contract = contratto.is_valid()
					if is_valid_contract:
						login(request, user)
						return HttpResponse()
					else:
						return HttpResponse('Unauthorized - 1', status=401)
				else:
					return HttpResponse('Unauthorized - 2', status=401)
			else:
				return HttpResponse('Unauthorized - 4', status=401)
		else:
			return HttpResponse('Unauthorized - 3', status=401)

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

		return JsonResponse(partners, safe = False)


def get_percentuale(percentuale_marketing):
	if percentuale_marketing <= 6.0:
		percentuale = 1
	elif (percentuale_marketing > 6.0) and (percentuale_marketing < 12.0):
		percentuale = "1+"
	elif percentuale_marketing == 12.0:
		percentuale = 2
	elif (percentuale_marketing > 12.0) and (percentuale_marketing < 18.0):
		percentuale = "2+"
	elif percentuale_marketing == 18.0:
		percentuale = 3	
	elif (percentuale_marketing > 18.0) and (percentuale_marketing < 24.0):
		percentuale = "3+"
	elif percentuale_marketing == 24.0:
		percentuale = 4	
	elif (percentuale_marketing > 24.0) and (percentuale_marketing < 30.0):
		percentuale = "4+"
	elif percentuale_marketing == 30.0:
		percentuale = 5	
	elif (percentuale_marketing > 30.0) and (percentuale_marketing < 36.0):
		percentuale = "5+"
	elif percentuale_marketing == 36.0:
		percentuale = 6	
	elif (percentuale_marketing > 36.0) and (percentuale_marketing < 42.0):
		percentuale = "6+"
	elif percentuale_marketing == 42.0:
		percentuale = 7	
	elif (percentuale_marketing > 42.0) and (percentuale_marketing < 48.0):
		percentuale = "7+"
	elif percentuale_marketing == 48.0:
		percentuale = 8	
	elif (percentuale_marketing > 48.0) and (percentuale_marketing < 54.0):
		percentuale = "8+"
	elif percentuale_marketing == 54.0:
		percentuale = 9	
	elif (percentuale_marketing > 54.0) and (percentuale_marketing < 60.0):
		percentuale = "9+"
	elif percentuale_marketing == 60.0:
		percentuale = 10
	elif (percentuale_marketing > 60.0) and (percentuale_marketing < 66.0):
		percentuale = "10+"
	elif percentuale_marketing == 66.0:
		percentuale = 11
	elif (percentuale_marketing > 66.0) and (percentuale_marketing < 72.0):
		percentuale = "11+"
	elif percentuale_marketing == 72.0:
		percentuale = 12
	elif (percentuale_marketing > 72.0) and (percentuale_marketing < 78.0):
		percentuale = "12+"
	elif percentuale_marketing == 78.0:
		percentuale = 13
	elif (percentuale_marketing > 78.0) and (percentuale_marketing < 84.0):
		percentuale = "13+"
	elif percentuale_marketing == 84.0:
		percentuale = 14
	elif (percentuale_marketing > 84.0) and (percentuale_marketing < 90.0):
		percentuale = "14+"
	elif percentuale_marketing == 90.0:
		percentuale = 15
	elif (percentuale_marketing > 90.0) and (percentuale_marketing < 96.0):
		percentuale = "15+"
	elif percentuale_marketing == 96.0:
		percentuale = 16

	return percentuale

class azienda_id(View):
	def dispatch(self, *args, **kwargs):
		return super(azienda_id, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):	

		su = Partner.objects.get(id = id)

		contratto = ContrattoMarketing.objects.get(partners = su)
		percentuale_marketing = contratto.percentuale_marketing	

		percentuale = get_percentuale(percentuale_marketing)

		json_su = {
			"id" : su.id,
			"foto" : str(su.foto),
			"descrizione" : su.descrizione,
			"telefono" : su.telefono_fisso,
			"ragione_sociale" : su.ragione_sociale,
			"indirizzo" : su.indirizzo,
			"tribu" : su.tribu,
			"percentuale" : percentuale
		}

		return JsonResponse(json_su)


class azienda_pagamento(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(azienda_pagamento, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):	
		user = request.user
		username = user.username
		#username = "868051020276493"
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

		notifica_pagamento(utente, pp, partner.ragione_sociale)

		if utente.tribu:
			tribu_utente = utente.tribu.nome

			if tribu_utente == "volpi":
				volpi_old = partner.volpi
				partner.volpi = volpi_old + pp

			elif tribu_utente == "puma":
				puma_old = partner.puma
				partner.puma = puma_old + pp	

			elif tribu_utente == "lupi":
				lupi_old = partner.lupi
				partner.lupi = lupi_old + pp

			elif tribu_utente == "aquile":
				aquile_old = partner.aquile
				partner.aquile = aquile_old + pp				
			elif tribu_utente == "orsi":
				orsi_old = partner.orsi
				partner.orsi = orsi_old + pp	

			partner.save()

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
	Pe = (Pe/100)

	E = float(acquisto.importo)
	Cp = 0.001

	Mt = calcola_Mt(tribu_utente, tribu_partner)

	Pp = ((E * Pe) * Mt) / Cp
	return Pp


from .tasks import salute, check_tribu
def test(request):
	#check_tribu()
	return HttpResponse("Successo!!!")


