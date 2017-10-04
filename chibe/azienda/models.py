# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from main.models import Tribu, Utente
from datetime import date, datetime
from haversine import haversine

class Categoria(models.Model):
	nome = models.CharField(max_length = 300)
	id_immagine = models.CharField(max_length = 300)

	def __unicode__(self):
		return self.nome	

	class Meta:
		verbose_name = "Categoria"
		verbose_name_plural = "Categorie"


class SearchQueryset(models.query.QuerySet):
	def search(self, lat, lon, limite):
		lat = float(lat)
		lon = float(lon)
		limite = float(limite)
		center_point = (lat, lon)

		result_list = []
		dict_distanza = {}
		now = datetime.now().date()

		for su in self:

			esiste_contratto = ContrattoMarketing.objects.filter(inizio__lte = now, fine__gte = now, partners = su).exists()
			if esiste_contratto:
				point = (su.latitudine, su.longitudine)
				distanza = haversine(center_point, point)

				if distanza < limite:

					orsi = su.orsi
					aquile = su.aquile
					lupi = su.lupi
					puma = su.puma
					volpi = su.volpi
					tribu = su.tribu
					tribu_val = None
					if tribu:
						tribu_val = tribu.nome

					json_su = {
						"id" : su.id,
						"foto" : str(su.foto),
						"descrizione" : su.descrizione,
						"telefono" : su.telefono_fisso,
						"ragione_sociale" : su.ragione_sociale,
						"indirizzo" : su.indirizzo,
						"distanza" : distanza,
						"orsi" : orsi,
						"aquile" : aquile,
						"lupi" : lupi,
						"puma" : puma,
						"volpi" : volpi,
						"tribu" : tribu_val
					}

					result_list.append(json_su)

		return result_list

class PartneroManager(models.Manager):
	def get_queryset(self):
		return SearchQueryset(self.model, using=self._db)

	def search(self, lat, lon, limite):
		return self.get_queryset().search(lat, lon, limite)

class Partner(User):
	objects_search = PartneroManager()
	ragione_sociale = models.CharField(max_length = 300, blank = True, null = True)
	codice_fiscale = models.CharField(max_length = 300, blank = True, null = True)
	partita_iva = models.CharField(max_length = 300, blank = True, null = True)
	indirizzo = models.CharField(max_length = 300, blank = True, null = True)
	latitudine = models.FloatField(blank = True, null = True)
	longitudine = models.FloatField(blank = True, null = True)
	telefono_fisso = models.CharField(max_length = 300, blank = True, null = True)
	telefono_cellulare = models.CharField(max_length = 300, blank = True, null = True)
	descrizione = models.TextField(blank = True, null = True)
	categorie = models.ManyToManyField(Categoria)
	foto = models.ImageField(blank = True, null = True)
	attivo = models.BooleanField(default = True) 

	is_fornitore = models.BooleanField(default = False)
	famoco_id = models.CharField(max_length = 300, blank = True, null = True)
	tribu = models.ForeignKey(Tribu, blank = True, null = True)

	orsi = models.IntegerField(default=0)
	aquile = models.IntegerField(default=0)
	lupi = models.IntegerField(default=0)
	puma = models.IntegerField(default=0)
	volpi = models.IntegerField(default=0)	

	def __unicode__(self):
		return self.ragione_sociale

	class Meta:
		verbose_name = "Partner"
		verbose_name_plural = "Partners"

	@staticmethod
	def post_save(sender, **kwargs):
		instance = kwargs.get('instance')
		created = kwargs.get('created')
		if created:
			username = instance.username
			instance.set_password(username)
			instance.save()

post_save.connect(Partner.post_save, sender=Partner)


class Supervisore(models.Model):
	etichetta = models.CharField(max_length = 300, blank = True, null = True)
	descrizione = models.TextField(blank = True, null = True)
	token = models.CharField(max_length = 300, blank = True, null = True)
	partner = models.ManyToManyField(Partner)

	class Meta:
		verbose_name = "Supervisore"
		verbose_name_plural = "Supervisori"

class Acquisto(models.Model):
	categoria = models.ForeignKey(Categoria)
	importo = models.DecimalField(max_digits=10, decimal_places=2)
	partner = models.ForeignKey(Partner) 
	utente = models.ForeignKey(Utente) 
	timestamp = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return str(self.importo)

	class Meta:
		verbose_name = "Acquisto"
		verbose_name_plural = "Acquisti"

class ContrattoMarketing(models.Model):
	partners = models.ManyToManyField(Partner)
	percentuale_marketing = models.FloatField(default = 0)

	# PERCENTUALE_LIST = (
	# 	("5", "x1"),
	# 	("10", "x2"),
	# 	("15", "x3"),
	# 	("20", "x4"),
	# 	("25", "x5"),
	# 	("30", "x6"),
	# 	("35", "x7"),
	# 	("40", "x8"),
	# 	("45", "x9"),
	# 	("45", "x10"),
	# )

	# percentuale_marketing = models.CharField(max_length = 2, choices = PERCENTUALE_LIST, default = "5")	

	inizio = models.DateField()
	fine = models.DateField()
	tacito_rinnovo = models.BooleanField(default = True)

	PERIODO_FATTURAZIONE = (
		("15", "15 giorni"),
		("30", "30 giorni"),
		("60", "60 giorni"),
		("90", "90 giorni"),
	)

	fatturazione = models.CharField(max_length = 3, choices = PERIODO_FATTURAZIONE, default = "15")	
	documentazione_traffico_acquisti = models.BooleanField(default = True)
	periodo_documentazione = models.CharField(max_length = 3, choices = PERIODO_FATTURAZIONE, default = "15")	

	def is_valid(self):
		fine = self.fine
		today = date.today()

		return today < fine

