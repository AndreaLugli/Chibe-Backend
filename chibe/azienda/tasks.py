from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Partner, Acquisto, ContrattoMarketing, Fattura
from main.models import Tribu
from datetime import date, datetime, timedelta
from chibe.push import push_generic
from django.db.models import Sum
from django.utils import timezone
import csv
import StringIO
from django.core.mail import EmailMultiAlternatives

import pytz
import requests
import time

FATTURE_CLOUD_API_UID = 113399
FATTURE_CLOUD_API_KEY = "441a70874e93291e5862776149024105"
FATTURE_CLOUD_ENDPOINT = "https://api.fattureincloud.it/v1"

@shared_task
def salute():
	print "Ciao!"

@shared_task
def notifica_perdenti(p, old_t):
	now = datetime.now()
	last_week = now - timedelta(days=7)

	ac = Acquisto.objects.filter(partner = p, utente__tribu = old_t, timestamp__gte=last_week, timestamp__lte=now)
	for a in ac:
		utente = a.utente

@shared_task
def notifica_vincenti(p, t):
	now = datetime.now()
	last_week = now - timedelta(days=7)

	ac = Acquisto.objects.filter(partner = p, utente__tribu = t, timestamp__gte=last_week, timestamp__lte=now)
	for a in ac:
		utente = a.utente

@shared_task
def check_tribu():
	all_p = Partner.objects.all()
	for p in all_p:
		list_valori = [
			{"nome" : "orsi", "punti" : p.orsi},
			{"nome" : "aquile", "punti" : p.aquile},
			{"nome" : "lupi", "punti" : p.lupi},
			{"nome" : "puma", "punti" : p.puma},
			{"nome" : "volpi", "punti" : p.volpi},
		]

		list_valori = sorted(list_valori, key=lambda k: k['punti'], reverse=True)

		primo = list_valori[0]
		nome_primo = primo['nome']
		punti_primo = primo['punti']

		t = Tribu.objects.get(nome = nome_primo)
		old_t = p.tribu

		if t != old_t:
			p.tribu = t
			p.save()
			notifica_perdenti(p, old_t)
			notifica_vincenti(p, t)

@shared_task
def check_fatturazione():
	today = date.today()

	partners = Partner.objects.select_related("contratto").filter(attivo = True)
	for p in partners:
		contratto = p.contratto
		is_valid = contratto.is_valid()
		if is_valid:
			date_fatturazione = contratto.date_fatturazione()
			if today in date_fatturazione:
				index_today = date_fatturazione.index(today)
				if index_today > 0:

					index_last = index_today - 1
					last_item = date_fatturazione[index_last]

					ragione_sociale = p.ragione_sociale
					partita_iva = p.partita_iva
					codice_fiscale = p.codice_fiscale
					indirizzo = p.indirizzo
					full_name = p.get_full_name()
					email = p.email

					inizio = contratto.inizio
					
					descrizione = "Contratto marketing del %s - Periodo di fatturazione dal giorno %s al giorno %s" % (inizio.strftime("%d/%m/%Y"), last_item.strftime("%d/%m/%Y"), today.strftime("%d/%m/%Y")) 

					oggetto_email = "Report movimenti Chibe periodo dal %s al %s" % (last_item.strftime("%d/%m/%Y"), today.strftime("%d/%m/%Y"))

					#importo_speso_totale = Acquisto.objects.filter(partner = p, timestamp__lte=today, timestamp__gt=last_item).aggregate(Sum('importo'))['importo__sum']
					
					tutti_acquisti = Acquisto.objects.filter(partner = p, timestamp__lte=today, timestamp__gt=last_item)

					importo_speso_totale = tutti_acquisti.aggregate(Sum('importo'))['importo__sum']

					percentuale_marketing = contratto.percentuale_marketing

					if importo_speso_totale:
						commissione = float(importo_speso_totale) * (percentuale_marketing / 100)
						commissione = round(commissione, 2)

						iva = commissione * (0.22)
						commissione_con_iva = commissione + iva
						commissione_con_iva = round(commissione_con_iva, 2)

						# print "--- Contratto Marketing ----"
						# print ragione_sociale
						# print partita_iva
						# print codice_fiscale
						# print indirizzo
						# print full_name
						# print email
						# print descrizione
						# print "Totale speso: "
						# print importo_speso_totale
						# print "Commissione: "
						# print commissione
						# print commissione_con_iva
						# print "----------------------------"

						url = FATTURE_CLOUD_ENDPOINT + "/fatture/nuovo"

						data = {
							"api_uid" : FATTURE_CLOUD_API_UID,
							"api_key" : FATTURE_CLOUD_API_KEY,
							"nome" : ragione_sociale,
							"indirizzo_via" : indirizzo,
							"piva" : partita_iva,
							"cf" : codice_fiscale,
							"autocompila_anagrafica" : True,
							"salva_anagrafica" : True,
							"data" : today.strftime("%d/%m/%Y"),
							"prezzi_ivati" : False,
							"email" : email,
							"lista_articoli" : [
								{
									"nome" : "Chibe",
									"descrizione" : descrizione,
									"prezzo_netto" : commissione,
									"prezzo_lordo" : commissione_con_iva,
									"cod_iva": 0
								}
							],
							"lista_pagamenti" : [
								{
									"data_scadenza" : today.strftime("%d/%m/%Y"),
									"data_saldo" : today.strftime("%d/%m/%Y"),
									"importo" : "auto",
									"metodo" : "not",
								}
							]
						}

						r = requests.post(url, json=data)
						#print r.json()
						#time.sleep(3)
						#email_fattura(p, tutti_acquisti, oggetto_email)
						email_fattura(partner, tutti_acquisti, oggetto_email).delay()

@shared_task
def email_fattura(partner, acquisti, oggetto_email):

	nome = partner.get_full_name()
	ragione_sociale = partner.ragione_sociale
	indirizzo = partner.indirizzo
	email = partner.email

	testo_email = "\
		Gentile %s,<br>\
		in allegato trova il report periodico con i movimenti fatti dai nostri Chibers nel suo locale %s in %s.<br><br>\
		Per qualunque informazione non esiti a contattarci alla nostra email info@chibe.it<br><br>\
		A presto,<br>\
		Il team di Chibe" % (nome, ragione_sociale, indirizzo)

	csvfile = StringIO.StringIO()
	csvwriter = csv.writer(csvfile)

	csvwriter.writerow(['codice utente', 'data', 'importo', 'FAMOCO'])

	for acquisto in acquisti:
		utente = acquisto.utente
		timestamp = acquisto.timestamp
		p = acquisto.partner

		codice_utente = utente.codice
		data = timestamp.strftime("%d/%m/%Y %H:%M:%S")
		importo = acquisto.importo
		famoco = p.username

		csvwriter.writerow([codice_utente, data, importo, famoco])

	from_email = 'chibe@chibeapp.com'
	to = email
	to = "senblet@gmail.com"
	subject = oggetto_email

	nomefile = "movimenti.csv"

	html_content = testo_email
	text_content = html_content
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html") 
	msg.attach(nomefile, csvfile.getvalue(), 'text/csv')       
	msg.send()








