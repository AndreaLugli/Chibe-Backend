from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Partner, Acquisto, ContrattoMarketing, Fattura
from main.models import Tribu
from datetime import date, datetime, timedelta
from chibe.push import push_generic
from django.db.models import Sum

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


#To delete?
@shared_task
def period_check_15():
	today = date.today()
	
	today = date(today.year, today.month, 15)

	today_day = today.day
	if today_day == 15:
		days_15_ago = today - timedelta(days=15)

		contratti = ContrattoMarketing.objects.filter(fatturazione = today_day)
		for contratto in contratti:
			is_valid = contratto.is_valid()
			if is_valid:
				partners = Partner.objects.filter(contratto = contratto, attivo = True)
				if partners:
					for partner in partners:
						importo_sum = Acquisto.objects.filter(partner = partner, timestamp__lte=today, timestamp__gte=days_15_ago).aggregate(Sum('importo'))['importo__sum']

						Fattura.objects.create(partner = partner, periodo_iniziale = days_15_ago, periodo_finale = today, importo = importo_sum)


@shared_task
def check_fatturazione():
	today = date.today()

	partners = Partner.objects.select_related("contratto").filter(attivo = True)
	for p in partners:
		contratto = p.contratto
		is_valid = contratto.is_valid()
		if is_valid:
			date_fatturazione = contratto.date_fatturazione()
			print date_fatturazione
			if today in date_fatturazione:
				print "YES"








