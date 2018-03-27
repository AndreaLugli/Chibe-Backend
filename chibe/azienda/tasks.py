from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Partner, Acquisto, ContrattoMarketing, Fattura
from main.models import Tribu
from datetime import date, datetime, timedelta
from chibe.push import push_generic
from django.db.models import Sum
import csv
import StringIO
from django.core.mail import EmailMultiAlternatives

import requests
import json
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
	cc = "info@chibe.it"
	subject = oggetto_email

	nomefile = "movimenti.csv"

	html_content = testo_email
	text_content = html_content
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to, cc])
	msg.attach_alternative(html_content, "text/html") 
	msg.attach(nomefile, csvfile.getvalue(), 'text/csv')       
	msg.send()


@shared_task
def genera_fattura():
	today = date.today()
	today_str = today.strftime("%d/%m/%Y") 

	oggi = today.day
	giorno_fatturazione = 5
	if oggi == giorno_fatturazione:
		first = today.replace(day = 1)
		ultimoMese = first - timedelta(days = 1)
		ultimoMese_str = ultimoMese.strftime("%d/%m/%Y")

		data_scadenza = today.replace(day = 15).strftime("%d/%m/%Y")

		mese = ultimoMese.month
		anno = ultimoMese.year

		partners = Partner.objects.select_related("contratto").filter(attivo = True)
		for p in partners:
			contratto = p.contratto
			inizio = contratto.inizio
			is_valid = contratto.is_valid()
			if is_valid:
				tutti_acquisti = Acquisto.objects.filter(partner = p, timestamp__month = mese, timestamp__year = anno)

				if tutti_acquisti:

					primoMese = ultimoMese.replace(day = 1)
					primoMese_str = primoMese.strftime("%d/%m/%Y")

					descrizione = "Contratto marketing del %s - Periodo di fatturazione dal giorno %s al giorno %s" % (inizio.strftime("%d/%m/%Y"), primoMese_str, ultimoMese_str) 

					oggetto_email = "Fattura Chibe periodo dal %s al %s" % (primoMese_str, ultimoMese_str)
					resoconto_email = "Report movimenti Chibe periodo dal %s al %s" % (primoMese_str, ultimoMese_str)

					importo_speso_totale = tutti_acquisti.aggregate(Sum('importo'))['importo__sum']

					percentuale_marketing = contratto.percentuale_marketing

					ragione_sociale = p.ragione_sociale
					partita_iva = p.partita_iva
					codice_fiscale = p.codice_fiscale
					indirizzo = p.indirizzo
					email = p.email

					if importo_speso_totale:
						commissione = float(importo_speso_totale) * (percentuale_marketing / 100)
						commissione = round(commissione, 2)

						iva = commissione * (0.22)
						commissione_con_iva = commissione + iva
						commissione_con_iva = round(commissione_con_iva, 2)

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
							"data" : today_str,
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
									"data_scadenza" : data_scadenza,
									"data_saldo" : today_str,
									"importo" : "auto",
									"metodo" : "not",
								}
							],
							"mostra_info_pagamento": True,
							"metodo_pagamento": "Bonifico",
							"metodo_titoloN": "IBAN",
							"metodo_descN": "IT76I0538702415000002570502",
							"extra_anagrafica": {
								"mail": email
							},
						}

						data = json.dumps(data)

						r = requests.post(url, data=data)
						output = r.json()

						new_id = output['new_id']

						invio_email_fic(new_id, email, oggetto_email, descrizione)
						email_fattura(p, tutti_acquisti, resoconto_email)
						time.sleep(3)


def invio_email_fic(id, mail_destinatario, oggetto, messaggio):
	url = FATTURE_CLOUD_ENDPOINT + "/fatture/inviamail"

	data = {
		"api_uid" : FATTURE_CLOUD_API_UID,
		"api_key" : FATTURE_CLOUD_API_KEY,	
		"id" : id,
		"mail_mittente" : "chibe@chibeapp.com",
		"mail_destinatario" : mail_destinatario,
		"oggetto" : oggetto,
		"messaggio" : messaggio,
		"allega_pdf" : True
	}

	data = json.dumps(data)

	r = requests.post(url, data=data)
	output = r.json()
	print output




