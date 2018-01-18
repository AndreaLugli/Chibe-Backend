# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core import serializers
from chibe.push import notifica_pagamento
from chibe.utils import get_percentuale
from datetime import timedelta, datetime
from django.utils import timezone
from azienda.models import Partner, Categoria, Acquisto
from main.models import Tribu, Utente, OrdineDesiderio

import logging
logger = logging.getLogger('django.request')

def azienda_index(request):
	return HttpResponse()

class azienda_login(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(azienda_login, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		imei = request.POST.get("imei", None)

		logger.debug(request.POST)

		user = authenticate(request, username=imei, password=imei)

		if user is not None:
			username = user.username
			partner = Partner.objects.get(username = username)

			attivo = partner.attivo
			if attivo:
				contratto = partner.contratto
				if contratto:
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
		user = request.user
		username = user.username
		partner = Partner.objects.get(username = username)
		
		categorie = partner.categorie.all()
		data = serializers.serialize('json', categorie, fields=('id', 'nome','id_immagine'))

		return HttpResponse(data)

class azienda_fornitore(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(azienda_fornitore, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		user = request.user
		username = user.username
		partner = Partner.objects.get(username = username)
		is_fornitore = partner.is_fornitore

		if is_fornitore:
			return HttpResponse()
		else:
			return HttpResponseBadRequest()

class azienda_premio(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(azienda_premio, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		user = request.user
		username = user.username
		partner = Partner.objects.get(username = username)
		token = request.POST['token']
		token = token.replace(" ", "").strip()

		ordine_ex = OrdineDesiderio.objects.filter(token = token).exists()

		if ordine_ex:
			ordine_obj = OrdineDesiderio.objects.get(token = token)
			ritirato = ordine_obj.ritirato

			if ritirato:
				return HttpResponseBadRequest("Premio già ritirato")
			else:
				desiderio = ordine_obj.gruppo.desiderio
				partners = desiderio.partners.all()

				if partner in partners:
					now = datetime.now()
					ordine_obj.ritirato = True
					ordine_obj.timestamp_ritiro = now
					ordine_obj.partner_ritirato = partner
					ordine_obj.save()

					desiderio_json = {
						"id" : desiderio.id,
						"nome" : desiderio.nome,
						"descrizione_lunga" : desiderio.descrizione_lunga,
						"immagine" : str(desiderio.immagine),
						"num_gruppo" : desiderio.num_gruppo,
						"punti_piuma" : desiderio.punti_piuma()
					}

					return JsonResponse(desiderio_json, safe = False)
				else:
					return HttpResponseBadRequest("Premio non disponibile nell'attività")
		else:
			return HttpResponseBadRequest("Codice errato")



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import itemgetter
class azienda_search(View):
	def dispatch(self, *args, **kwargs):
		return super(azienda_search, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):	

		latitude = request.GET['latitude']
		longitude = request.GET['longitude']
		distanza = float(10)

		partners = Partner.objects_search.search(latitude, longitude, distanza)

		order = request.GET.get("order", "vicini")

		if order == "vicini":
			partners = sorted(partners, key=itemgetter('distanza'))
		elif order == "promo":
			partners = sorted(partners, key=itemgetter('percentuale_val'), reverse = True)
		elif order == "news":
			partners = sorted(partners, key=itemgetter('date_joined'), reverse = True)
		elif order == "combattuti":
			partners = sorted(partners, key=itemgetter('importo'), reverse = True)
		elif order == "tribu":
			user = request.user
			username = user.username
			utente = Utente.objects.get(username = username)
			tribu = utente.tribu
			if tribu:
				tribu_val = tribu.nome
				partners = [d for d in partners if d['tribu'] == tribu_val]

		paginator = Paginator(partners, 10)

		page = request.GET.get("page")

		if page == "null":
			page = 1

		try:
			partners_list = paginator.page(page)
		except PageNotAnInteger:
			partners_list = paginator.page(1)
		except EmptyPage:
			partners_list = []

		if partners_list:
			partners_output = partners_list.object_list
		else:
			partners_output = []

		return JsonResponse(partners_output, safe = False)

def get_campo_di_battaglia(su):
	some_day_last_week = timezone.now().date() - timedelta(days=7)

	aquisti = Acquisto.objects.select_related("utente", "utente__tribu").filter(partner = su, timestamp__gte = some_day_last_week)

	if aquisti:

		volpi = 0
		puma = 0
		lupi = 0
		aquile = 0
		orsi = 0

		for aq in aquisti:
			importo = aq.importo
			utente = aq.utente
			tribu = utente.tribu

			if tribu:
				tribu_val = tribu.nome
				if tribu_val == "volpi":
					volpi = volpi + importo
				elif tribu_val == "puma":
					puma = puma + importo
				elif tribu_val == "lupi":
					lupi = lupi + importo
				elif tribu_val == "aquile":
					aquile = aquile + importo
				elif tribu_val == "orsi":
					orsi = orsi + importo

		volpi_dict = {"nome" : "volpi", "totale" : volpi}
		puma_dict = {"nome" : "puma", "totale" : puma}
		lupi_dict = {"nome" : "lupi", "totale" : lupi}
		aquile_dict = {"nome" : "aquile", "totale" : aquile}
		orsi_dict = {"nome" : "orsi", "totale" : orsi}

		list_tribu = [volpi_dict, puma_dict, lupi_dict, aquile_dict, orsi_dict]
		newlist = sorted(list_tribu, key=lambda k: k['totale'], reverse=True) 

		return newlist[0]['nome'], newlist[1]['nome']
	else:
		print "NO"
		return None, None

class azienda_id(View):
	def dispatch(self, *args, **kwargs):
		return super(azienda_id, self).dispatch(*args, **kwargs)

	def get(self, request, id, *args, **kwargs):	

		su = Partner.objects.get(id = id)

		contratto = su.contratto
		percentuale_marketing = contratto.percentuale_marketing	

		percentuale = get_percentuale(percentuale_marketing)

		tribu_1, tribu_2 = get_campo_di_battaglia(su)

		tribu = su.tribu
		tribu_str = None
		if tribu:
			tribu_str = tribu.nome

		json_su = {
			"id" : su.id,
			"logo" : str(su.logo),
			"banner" : str(su.banner),
			"descrizione" : su.descrizione,
			"telefono" : su.telefono_fisso,
			"ragione_sociale" : su.ragione_sociale,
			"indirizzo" : su.indirizzo,
			"tribu" : tribu_str,
			"tribu_1" : tribu_1,
			"tribu_2" : tribu_2,
			"percentuale" : percentuale
		}

		return JsonResponse(json_su)

from django.utils import timezone
class azienda_pagamento(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(azienda_pagamento, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):	
		user = request.user
		username = user.username
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

		timestamp = timezone.now()

		ex_ac = Acquisto.objects.filter(
			categoria = categoria,
			importo = importo,
			partner = partner,
			utente = utente,
			timestamp = timestamp
		).exists()

		if ex_ac:
			return HttpResponse()
		
		new_acquisto = Acquisto.objects.create(
			categoria = categoria,
			importo = importo,
			partner = partner,
			utente = utente,
			timestamp = timestamp
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

	contratto = partner.contratto
	Pe = contratto.percentuale_marketing
	Pe = (Pe/100)

	E = float(acquisto.importo)
	Cp = 0.001

	Mt = calcola_Mt(tribu_utente, tribu_partner)

	Pp = ((E * Pe) * Mt) / Cp
	return Pp


from .tasks import salute, check_tribu, check_fatturazione
def test(request):
	check_fatturazione()
	return HttpResponse("Successo!!!")


