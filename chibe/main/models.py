# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from desideri.models import Desiderio

class Provincia(models.Model):
	nome = models.CharField(max_length = 200)
	codice = models.CharField(max_length = 2)
	attivo = models.BooleanField(default = True)

	def __unicode__(self):
		return self.nome

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

class Utente(User):
	avatar = models.CharField(max_length = 300, blank = True, null = True)
	classe = models.CharField(max_length = 300, blank = True, null = True)
	telefono_cellulare = models.CharField(max_length = 300, blank = True, null = True)
	descrizione = models.TextField(blank = True, null = True)

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
	tribu_timestamp = models.DateField(blank = True, null = True)

	amici = models.ManyToManyField("self", blank = True)

	#Login con Facebook (token)
	#Login con Google Account (token)

	class Meta:
		verbose_name = "Utente"
		verbose_name_plural = "Utente"

class Gruppo(models.Model):
	desiderio = models.ForeignKey(Desiderio)
	utente_admin = models.ForeignKey(Utente, related_name = "utente_admin")
	utenti = models.ManyToManyField(Utente, related_name = "utenti")
	punti = models.IntegerField(default = 0)

	class Meta:
		verbose_name = "Gruppo"
		verbose_name_plural = "Gruppi"	

class PuntiGruppo(models.Model):
	utente = models.ForeignKey(Utente, related_name = "utente_puntigruppo")
	gruppo = models.ForeignKey(Gruppo, related_name = "gruppo_puntigruppo")
	punti = models.IntegerField(default = 0)

class Rubrica(models.Model):
	utente = models.ForeignKey(Utente, related_name = "utente_gruppo")
	utenti = models.ManyToManyField(Utente, related_name = "utenti_gruppo")

	class Meta:
		verbose_name = "Rubrica"
		verbose_name_plural = "Rubriche"	

class OrdineDesiderio(models.Model):
	timestamp = models.DateTimeField(auto_now_add = True)
	gruppo = models.ForeignKey(Gruppo)
	partner_ritirato = models.ForeignKey("azienda.Partner", blank = True, null = True)

	class Meta:
		verbose_name = "Ordine desideiro"
		verbose_name_plural = "Ordini desideri"	


class OnBoard(models.Model):
	utente = models.ForeignKey(Utente)
	complete = models.BooleanField(default = False)
	step_1 = models.BooleanField(default = False, verbose_name = "Dati personali")
	step_2 = models.BooleanField(default = False, verbose_name = "Avatar")
	step_3 = models.BooleanField(default = False, verbose_name = "Provincia")

	def __unicode__(self):
		return self.utente.email



