# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class CategoriaPremio(models.Model):
	nome = models.CharField(max_length = 300)
	id_immagine = models.CharField(max_length = 300)
	descrizione = models.TextField(blank = True, null = True)

	def __unicode__(self):
		return self.nome	

	class Meta:
		verbose_name = "Categoria premio"
		verbose_name_plural = "Categorie premio"	

class Premio(models.Model):
	nome = models.CharField(max_length = 300, blank = True, null = True)
	descrizione_breve = models.TextField(blank = True, null = True)
	descrizione_lunga = models.TextField(blank = True, null = True)
	punti = models.IntegerField()
	immagine = models.CharField(max_length = 300, blank = True, null = True)
	categoria = models.ForeignKey(CategoriaPremio)
	data_inizio = models.DateField
	data_fine = models.DateField()
	in_evidenza = models.BooleanField(default = False)
	sku = models.IntegerField()

	indirizzo = models.CharField(max_length = 300, blank = True, null = True)
	latitudine = models.CharField(max_length = 300, blank = True, null = True)
	longitudine = models.CharField(max_length = 300, blank = True, null = True)

	codice = models.CharField(max_length = 300, blank = True, null = True)
	num_gruppo = models.IntegerField()

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Premio"
		verbose_name_plural = "Premi"	



