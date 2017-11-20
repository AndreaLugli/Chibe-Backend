from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Gruppo, PuntiGruppo, OrdineDesiderio
from chibe.push import notifica_restituzione, notifica_scadenza
from datetime import datetime

@shared_task
def check_sku_groups(my_gruppo_id, desiderio):
	gruppi = Gruppo.objects.prefetch_related('utenti').filter(desiderio = desiderio).select_related('utente_admin').exclude(pk = my_gruppo_id)
	desiderio_str = desiderio.nome

	for gruppo in gruppi:
		
		utente_admin = gruppo.utente_admin
		punti_gruppo_admin_ex = PuntiGruppo.objects.filter(utente = utente_admin, gruppo = gruppo).exists()
		if punti_gruppo_admin_ex:
			notifica_restituzione(utente_admin, desiderio_str)
			punti_admin = PuntiGruppo.objects.filter(utente = utente_admin, gruppo = gruppo)
			for pp in punti_admin:
				punti = pp.punti
				punti_old = utente_admin.punti
				punti_new = punti_old + punti
				utente_admin.punti = punti_new
				utente_admin.save()				

		utenti = gruppo.utenti.all()
		for utente in utenti:
			punti_gruppo_ex = PuntiGruppo.objects.filter(utente = utente, gruppo = gruppo).exists()
			if punti_gruppo_ex:
				notifica_restituzione(utente, desiderio_str)
				punti_gruppo = PuntiGruppo.objects.filter(utente = utente, gruppo = gruppo)
				for punto_gruppo in punti_gruppo:
					punti = punto_gruppo.punti
					punti_old = utente.punti
					punti_new = punti_old + punti
					utente.punti = punti_new
					utente.save()
					punti_gruppo.delete()

		gruppo.delete()

@shared_task
def check_desiderio_scaduto():
	now = datetime.now().date()
	desideri = Desiderio.objects.filter(data_fine__lte = now)	
	for desiderio in desideri:
		gruppi = Gruppo.objects.prefetch_related('utenti').filter(desiderio = desiderio).select_related('utente_admin')
		desiderio_str = desiderio.nome

		for gruppo in gruppi:
			
			utente_admin = gruppo.utente_admin
			punti_gruppo_admin_ex = PuntiGruppo.objects.filter(utente = utente_admin, gruppo = gruppo).exists()
			if punti_gruppo_admin_ex:
				notifica_scadenza(utente_admin, desiderio_str)
				punti_admin = PuntiGruppo.objects.filter(utente = utente_admin, gruppo = gruppo)
				for pp in punti_admin:
					punti = pp.punti
					punti_old = utente_admin.punti
					punti_new = punti_old + punti
					utente_admin.punti = punti_new
					utente_admin.save()				

			utenti = gruppo.utenti.all()
			for utente in utenti:
				punti_gruppo_ex = PuntiGruppo.objects.filter(utente = utente, gruppo = gruppo).exists()
				if punti_gruppo_ex:
					notifica_scadenza(utente, desiderio_str)
					punti_gruppo = PuntiGruppo.objects.filter(utente = utente, gruppo = gruppo)
					for punto_gruppo in punti_gruppo:
						punti = punto_gruppo.punti
						punti_old = utente.punti
						punti_new = punti_old + punti
						utente.punti = punti_new
						utente.save()
						punti_gruppo.delete()

			gruppo.delete()


