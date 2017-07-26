# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from main.models import Tribu, Studente

class Categoria(models.Model):
	nome = models.CharField(max_length = 300)
	id_immagine = models.CharField(max_length = 300)

	def __unicode__(self):
		return self.nome	

	class Meta:
		verbose_name = "Categoria"
		verbose_name_plural = "Categorie"

class Esercente(User):
	ragione_sociale = models.CharField(max_length = 300, blank = True, null = True)
	indirizzo = models.CharField(max_length = 300, blank = True, null = True)
	latitudine = models.CharField(max_length = 300, blank = True, null = True)
	longitudine = models.CharField(max_length = 300, blank = True, null = True)
	telefono_fisso = models.CharField(max_length = 300, blank = True, null = True)
	telefono_cellulare = models.CharField(max_length = 300, blank = True, null = True)
	descrizione = models.TextField(blank = True, null = True)
	categorie = models.ManyToManyField(Categoria)

	STATUS = (
		("ABI", "Abilitato"),
		("BLO", "Bloccato"),
	)

	status = models.CharField(max_length = 3, choices = STATUS, default = "ABI")
	is_fornitore = models.BooleanField(default = False)
	famoco_id = models.CharField(max_length = 300, blank = True, null = True)
	tribu = models.ForeignKey(Tribu, blank = True, null = True)

	# Totale punti spesi Tribù 1
	# Totale punti spesi Tribù 2
	# Totale punti spesi Tribù 3
	# Totale punti spesi Tribù 4
	# Totale punti spesi Tribù 5 (da definire le tribù)


	def __unicode__(self):
		return self.ragione_sociale

	class Meta:
		verbose_name = "Esercente"
		verbose_name_plural = "Esercenti"

class Supervisore(models.Model):
	etichetta = models.CharField(max_length = 300, blank = True, null = True)
	descrizione = models.TextField(blank = True, null = True)
	token = models.CharField(max_length = 300, blank = True, null = True)
	esercenti = models.ManyToManyField(Esercente)

	class Meta:
		verbose_name = "Supervisore"
		verbose_name_plural = "Supervisori"

class Acquisto(models.Model):
	categoria = models.ForeignKey(Categoria)
	importo = models.DecimalField(max_digits=10, decimal_places=2)
	esercente = models.ForeignKey(Esercente) 
	studente = models.ForeignKey(Studente) 
	timestamp = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return self.importo

	class Meta:
		verbose_name = "Acquisto"
		verbose_name_plural = "Acquisti"

