from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Partner, Acquisto
from main.models import Tribu
from datetime import date, datetime, timedelta

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
		print utente

@shared_task
def notifica_vincenti(p, t):
	now = datetime.now()
	last_week = now - timedelta(days=7)

	ac = Acquisto.objects.filter(partner = p, utente__tribu = t, timestamp__gte=last_week, timestamp__lte=now)
	for a in ac:
		utente = a.utente
		print utente

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




