# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from premi.models import Premio

class Provincia(models.Model):
	nome = models.CharField(max_length = 2)
	attivo = models.BooleanField(default = True)

class Scuola(models.Model):
	nome = models.CharField(max_length = 300, blank = True, null = True)
	provincia = models.ForeignKey(Provincia, blank = True, null = True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Scuola"
		verbose_name_plural = "Scuole"	

class Tribu(models.Model):
	nome = models.CharField(max_length = 300, blank = True, null = True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Tribù"
		verbose_name_plural = "Tribù"	

class Studente(User):
	avatar = models.CharField(max_length = 300, blank = True, null = True)
	classe = models.CharField(max_length = 300, blank = True, null = True)
	telefono_cellulare = models.CharField(max_length = 300, blank = True, null = True)

	STATUS = (
		("ABI", "Abilitato"),
		("BLO", "Bloccato"),
	)

	status = models.CharField(max_length = 3, choices = STATUS, default = "ABI")
	codice = models.CharField(max_length = 300, blank = True, null = True)
	timestamp = models.DateTimeField(auto_now_add = True)
	punti = models.IntegerField(default = 0)

	provincia = models.ForeignKey(Provincia, blank = True, null = True)
	scuola = models.ForeignKey(Scuola, blank = True, null = True)
	tribu = models.ForeignKey(Tribu, blank = True, null = True)

	#Login con Facebook (token)
	#Login con Google Account (token)

	class Meta:
		verbose_name = "Studente"
		verbose_name_plural = "Studenti"

class Gruppo(models.Model):
	premio = models.ForeignKey(Premio)
	studente_admin = models.ForeignKey(Studente, related_name = "studente_admin")
	studenti = models.ManyToManyField(Studente, related_name = "studenti")

	class Meta:
		verbose_name = "Gruppo"
		verbose_name_plural = "Gruppi"	

class Rubrica(models.Model):
	studente = models.ForeignKey(Studente, related_name = "studente_gruppo")
	studenti = models.ManyToManyField(Studente, related_name = "studenti_gruppo")

	class Meta:
		verbose_name = "Rubrica"
		verbose_name_plural = "Rubriche"	

class OrdinePremio(models.Model):
	timestamp = models.DateTimeField(auto_now_add = True)
	gruppo = models.ForeignKey(Gruppo)

	class Meta:
		verbose_name = "Ordine premio"
		verbose_name_plural = "Ordini premio"	










