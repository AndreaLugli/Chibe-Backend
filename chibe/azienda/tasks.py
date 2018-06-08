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
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from desideri.models import AcquistoSpeciale, PremioSpeciale

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

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in xrange(0, len(l), n))

def print_table(p, data_chucked):
	data_chucked.pop(0)	
	for data in data_chucked:
		p.showPage()
		table = Table(data, colWidths=[4.75 * cm, 4.75 * cm, 4.75 * cm, 4.75 * cm])

		LIST_STYLE = TableStyle(
			[('LINEABOVE', (0,0), (-1,0), 2, colors.HexColor("#6DD0DD")),
			('LINEABOVE', (0,1), (-1,-1), 0.25, colors.HexColor("#6DD0DD")),
			('LINEBELOW', (0,-1), (-1,-1), 2, colors.HexColor("#6DD0DD")),
			('ALIGN', (-2,0), (-1,-1), 'CENTER')]
		)
		table.setStyle(LIST_STYLE)

		tw, th, = table.wrapOn(p, 15 * cm, 19 * cm)	
		table.drawOn(p, 1 * cm, 27.5 * cm - th)

def header_func(canvas):
	#logo = "/Users/riccardo/Desktop/Progetti/chibe/chibe/static/homepage.png"
	logo = "/home/django/static/homepage.png"

	canvas.setStrokeColorRGB(0.9, 0.5, 0.2)
	canvas.setFillColorRGB(0.2, 0.2, 0.2)
	canvas.setFont('Helvetica', 16)
	canvas.drawString(13 * cm, -2 * cm, 'Report transazioni Chibe')
	canvas.drawInlineImage(logo, 1 * cm, -3 * cm, 3 * cm, 3 * cm)

def address_func(canvas, partner):
    """ Draws the business address """
    business_details = (
        partner.ragione_sociale,
        partner.ragione_sociale_fattura,
        partner.indirizzo,
        partner.email,
        U'',
        U'',
        u'',
        u'',
        u'',
        u'',
        u'',
        u''
    )
    canvas.setFont('Helvetica', 9)
    textobject = canvas.beginText(13 * cm, -4 * cm)
    for line in business_details:
        textobject.textLine(line)
    canvas.drawText(textobject)

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

	buffer = BytesIO()

	p = canvas.Canvas(buffer, pagesize=A4)

	p.translate(0, 29.7 * cm)
	p.setFont('Helvetica', 10)

	p.saveState()
	header_func(p)
	p.restoreState()

	p.saveState()
	address_func(p, partner)
	p.restoreState()

	# Chibe
	textobject = p.beginText(1.5 * cm, -4 * cm)
	contact_name = "Chibe S.r.l"
	textobject.textLine(contact_name)
	address_one = "Via Masi, 21"
	textobject.textLine(address_one)
	address_two = "40137 Bologna"
	textobject.textLine(address_two)
	town = "amministrazione@chibe.it"
	textobject.textLine(town)
	p.drawText(textobject)

	# Items
	data = [[u'Codice utente', u'Data', u'Importo', u'FAMOCO'], ]

	for item in acquisti:
		utente = item.utente
		timestamp = item.timestamp
		partner_obj = item.partner

		codice_utente = utente.codice
		data_obj = timestamp.strftime("%d/%m/%Y %H:%M:%S")
		importo = item.importo
		famoco = partner_obj.username

		data.append([codice_utente, data_obj, importo, famoco])

	# Chunk a 30
	data_chucked = chunks(data, 30)
	data_chucked = list(data_chucked)

	data_1 = data_chucked[0]
	len_data_chuncked = len(data_chucked)

	table = Table(data_1, colWidths=[4.75 * cm, 4.75 * cm, 4.75 * cm, 4.75 * cm])

	LIST_STYLE = TableStyle(
		[('LINEABOVE', (0,0), (-1,0), 2, colors.HexColor("#6DD0DD")),
		('LINEABOVE', (0,1), (-1,-1), 0.25, colors.HexColor("#6DD0DD")),
		('LINEBELOW', (0,-1), (-1,-1), 2, colors.HexColor("#6DD0DD")),
		('ALIGN', (-2,0), (-1,-1), 'CENTER')]
	)
	table.setStyle(LIST_STYLE)

	tw, th, = table.wrapOn(p, 15 * cm, 19 * cm)
	table.drawOn(p, 1 * cm, -8 * cm - th)

	# Inizio chunk
	if len_data_chuncked > 1:
		print_table(p, data_chucked)
	# Fine chunk

	p.showPage()
	p.save()

	pdf = buffer.getvalue()
	buffer.close()

	from_email = 'chibe@chibeapp.com'
	to = email
	cc = "info@chibe.it"
	subject = oggetto_email

	nomefile = "movimenti.pdf"

	html_content = testo_email
	text_content = html_content
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to, cc])
	msg.attach_alternative(html_content, "text/html") 
	msg.attach(nomefile, pdf, 'text/csv')       
	msg.send()

@shared_task
def check_premiospeciale():
	today = date.today()
	yesterday = today - timedelta(days = 1)
	yesterday_str = yesterday.strftime("%d/%m/%Y") 

	partners = Partner.objects.select_related("contratto").filter(attivo = True)

	for partner_obj in partners:
		acquisti_speciali = AcquistoSpeciale.objects.select_related('premio').filter(timestamp__date = yesterday, premio__partner = partner_obj)
		if acquisti_speciali:
			num_acquisti_speciali = acquisti_speciali.count()
			premio_s = PremioSpeciale.objects.get(partner = partner_obj)

			desiderio_speciale_str = premio_s.nome
			rimanenze = premio_s.sku

			nome = partner_obj.get_full_name()
			ragione_sociale = partner_obj.ragione_sociale
			indirizzo = partner_obj.indirizzo
			email = partner_obj.email

			oggetto_email = "Report desideri speciali"

			testo_email = "\
				Gentile %s,<br>\
				in allegato trova il report giornaliero relativo alla data %s con gli acquisti del desiderio speciale '%s' fatti dai nostri Chibers nel suo locale %s in %s.<br><br>\
				Per qualunque informazione non esiti a contattarci alla nostra email info@chibe.it<br><br>\
				A presto,<br>\
				Il team di Chibe" % (nome, yesterday_str, desiderio_speciale_str, ragione_sociale, indirizzo)		

			buffer = BytesIO()

			p = canvas.Canvas(buffer, pagesize=A4)

			p.translate(0, 29.7 * cm)
			p.setFont('Helvetica', 10)

			p.saveState()
			header_func(p)
			p.restoreState()

			p.saveState()
			address_func(p, partner_obj)
			p.restoreState()

			# Chibe
			textobject = p.beginText(1.5 * cm, -4 * cm)
			contact_name = "Chibe S.r.l"
			textobject.textLine(contact_name)
			address_one = "Via Masi, 21"
			textobject.textLine(address_one)
			address_two = "40137 Bologna"
			textobject.textLine(address_two)
			town = "amministrazione@chibe.it"
			textobject.textLine(town)
			textobject.textLine("")
			unita_ri = "Desideri speciali ritirati: " + str(num_acquisti_speciali)
			textobject.textLine(unita_ri)
			unita_ri = "Desideri speciali rimanenti: " + str(rimanenze)
			textobject.textLine(unita_ri)			
			p.drawText(textobject)

			# Items
			data = [[u'Data', u'FAMOCO'], ]

			for item in acquisti_speciali:
				timestamp = item.timestamp
				partner_obj = item.premio.partner

				data_obj = timestamp.strftime("%d/%m/%Y %H:%M:%S")
				famoco = partner_obj.username

				data.append([data_obj, famoco])

			table = Table(data, colWidths=[4.75 * cm, 4.75 * cm, 4.75 * cm, 4.75 * cm])

			LIST_STYLE = TableStyle(
				[('LINEABOVE', (0,0), (-1,0), 2, colors.HexColor("#6DD0DD")),
				('LINEABOVE', (0,1), (-1,-1), 0.25, colors.HexColor("#6DD0DD")),
				('LINEBELOW', (0,-1), (-1,-1), 2, colors.HexColor("#6DD0DD")),
				('ALIGN', (-2,0), (-1,-1), 'CENTER')]
			)
			table.setStyle(LIST_STYLE)

			tw, th, = table.wrapOn(p, 15 * cm, 19 * cm)
			table.drawOn(p, 1 * cm, -8 * cm - th)

			p.showPage()
			p.save()

			pdf = buffer.getvalue()
			buffer.close()

			from_email = 'chibe@chibeapp.com'
			to = email
			cc = "info@chibe.it"
			subject = oggetto_email

			nomefile = "movimenti_speciali.pdf"

			html_content = testo_email
			text_content = html_content
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to, cc])
			msg.attach_alternative(html_content, "text/html") 
			msg.attach(nomefile, pdf, 'text/csv')       
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

					resoconto_email = "Report movimenti Chibe periodo dal %s al %s" % (primoMese_str, ultimoMese_str)

					importo_speso_totale = tutti_acquisti.aggregate(Sum('importo'))['importo__sum']

					percentuale_marketing = contratto.percentuale_marketing

					ragione_sociale = p.ragione_sociale
					ragione_sociale_fattura = p.ragione_sociale_fattura

					if ragione_sociale_fattura:
						ragione_sociale_str = ragione_sociale_fattura
					else:
						ragione_sociale_str = ragione_sociale

					partita_iva = p.partita_iva
					codice_fiscale = p.codice_fiscale
					indirizzo = p.indirizzo
					email = p.email
					indirizzo_via_fattura = p.indirizzo_via_fattura
					indirizzo_cap = p.indirizzo_cap
					indirizzo_citta = p.indirizzo_citta
					indirizzo_provincia = p.indirizzo_provincia
					indirizzo_extra = p.indirizzo_extra
					telefono_fisso = p.telefono_fisso
					fax = p.fax

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
							"nome" : ragione_sociale_str,
							"indirizzo_via" : indirizzo_via_fattura,
							"indirizzo_cap" : indirizzo_cap,
							"indirizzo_citta" : indirizzo_citta,
							"indirizzo_provincia" : indirizzo_provincia,
							"indirizzo_extra" : indirizzo_extra,
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
								"mail": email,
								"tel" : telefono_fisso,
								"fax" : fax
							},
						}

						data = json.dumps(data)

						r = requests.post(url, data=data)
						output = r.json()
						print output
						
						email_fattura(p, tutti_acquisti, resoconto_email)
						time.sleep(3)
						print "-"


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




