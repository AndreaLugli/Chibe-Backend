# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.db import models
from django.contrib.auth.models import User
from desideri.models import Desiderio

class Provincia(models.Model):
	nome = models.CharField(max_length = 200)
	codice = models.CharField(max_length = 2)
	attivo = models.BooleanField(default = True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Provincia"
		verbose_name_plural = "3. Provincie"			

class Scuola(models.Model):
	nome = models.CharField(max_length = 300, blank = True, null = True)
	provincia = models.ForeignKey(Provincia, blank = True, null = True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Scuola"
		verbose_name_plural = "2. Scuole"	

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

	SESSO = (
		("M", "Maschio"),
		("F", "Femmina"),
	)

	sesso = models.CharField(max_length = 3, choices = SESSO, default = "M")
	compleanno = models.DateField(blank=True, null=True)	

	def invite_link(self):
		invite_link_url = reverse('utente_invito', kwargs = {'token': self.codice})
		invite_link_str = '<a href="%s" target="_blank">%s</a>' % (invite_link_url, invite_link_url)
		return mark_safe(invite_link_str)
	invite_link.short_description = 'Invite link'

	class Meta:
		verbose_name = "Utente"
		verbose_name_plural = "1. Utente"

class Gruppo(models.Model):
	desiderio = models.ForeignKey(Desiderio)
	utente_admin = models.ForeignKey(Utente, related_name = "utente_admin")
	utenti = models.ManyToManyField(Utente, related_name = "utenti")
	punti = models.IntegerField(default = 0)

	def is_conquistato(self):
		punti = self.punti
		desiderio = self.desiderio
		punti_piuma = desiderio.punti_piuma()

		if punti >= punti_piuma:
			return True
		else:
			return False

	def __unicode__(self):
		return str(self.id)

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
	ritirato = models.BooleanField(default = False)
	timestamp_ritiro = models.DateTimeField(blank = True, null = True)
	token = models.CharField(max_length = 300)

	class Meta:
		verbose_name = "Ordine desideiro"
		verbose_name_plural = "Ordini desideri"	


class OnBoard(models.Model):
	utente = models.ForeignKey(Utente)
	complete = models.BooleanField(default = False)
	step_1 = models.BooleanField(default = False, verbose_name = "Dati personali")
	step_2 = models.BooleanField(default = False, verbose_name = "Avatar")
	step_3 = models.BooleanField(default = False, verbose_name = "Provincia")

	fb_step_1 = models.BooleanField(default = False, verbose_name = "Dati extra Facebook")
	fb_step_2 = models.BooleanField(default = False, verbose_name = "Provincia")
	fb_complete = models.BooleanField(default = False)

	def __unicode__(self):
		return self.utente.email

class ResetPassword(models.Model):
	user = models.ForeignKey(Utente)
	token = models.CharField(max_length = 300)
	used = models.BooleanField(default = False)

	class Meta:
		verbose_name = "Reset password"
		verbose_name_plural = "Reset password"

	def __unicode__(self):
		return self.user.get_full_name()

class PushNotification(models.Model):
	SISTEMI = (
		('Android', 'Android'),
		('iOS', 'iOS'),
		('WP', 'Windows Phone'),
	)
	utente = models.ForeignKey(Utente)
	sistema_operativo = models.CharField(max_length=7, choices=SISTEMI)
	token = models.CharField(max_length=300)

	class Meta:
		verbose_name = "Notifica push"
		verbose_name_plural = "Notifiche push"






