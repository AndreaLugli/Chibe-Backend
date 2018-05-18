# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
import unicodecsv as csv
from .models import Utente, OnBoard, Provincia, Scuola, Tribu, Gruppo, PushNotification, PuntiGruppo, OrdineDesiderio, ResetPassword
from chibe.tasks import send_push_gcm, send_push_apns
from django.http import HttpResponse

def test_push(modeladmin, request, queryset):
	content = "Test"
	for push in queryset:
		o_system = push.sistema_operativo
		token = push.token

		if o_system == "Android":
			send_push_gcm(token, content)
		else:
			send_push_apns(token, content, True)


def export_utente(modeladmin, request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="Utenti.csv"'

	writer = csv.writer(response)
	writer.writerow(['codice', 'username', 'tribu', 'punti', 'avatar', 'codice', 'email', 'first_name', 'last_name', 'telefono_cellulare', 'provincia', 'scuola', 'classe', 'sesso', 'compleanno', 'invite_link', 'date_joined'])

	for utente in queryset:
		codice = utente.codice
		username = utente.username
		tribu = utente.tribu
		punti = utente.punti
		avatar = utente.avatar
		codice = utente.codice
		email = utente.email
		first_name = utente.first_name
		last_name = utente.last_name
		telefono_cellulare = utente.telefono_cellulare
		provincia = utente.provincia
		scuola = utente.scuola
		classe = utente.classe
		sesso = utente.sesso
		compleanno = utente.compleanno
		invite_link = utente.invite_link
		date_joined = utente.date_joined

		writer.writerow([codice, username, tribu, punti, avatar, codice, email, first_name, last_name, telefono_cellulare, provincia, scuola, classe, sesso, compleanno, invite_link, date_joined])

	return response

@admin.register(Utente)
class UtenteAdmin(admin.ModelAdmin):
	list_display = ['codice', 'username', 'tribu', 'punti', 'avatar', 'codice', 'email', 'first_name', 'last_name', 'telefono_cellulare', 'provincia', 'scuola', 'classe', 'sesso', 'compleanno', 'invite_link', 'date_joined']
	fields = ('username', 'first_name', 'last_name', 'email', 'avatar', 'classe', 'telefono_cellulare', 'descrizione', 'status', 'codice', 'punti', 'provincia', 'scuola', 'tribu', 'tribu_timestamp', 'amici', 'sesso', 'compleanno')

	actions = [export_utente]


@admin.register(OnBoard)
class OnBoardAdmin(admin.ModelAdmin):
	list_display = ['utente', 'step_1', 'step_2', 'step_3', 'complete', 'fb_step_1', 'fb_step_2', 'fb_complete']

@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
	pass

@admin.register(Scuola)
class ScuolaAdmin(admin.ModelAdmin):
	pass

@admin.register(ResetPassword)
class ResetPasswordAdmin(admin.ModelAdmin):
	pass

@admin.register(Tribu)
class TribuAdmin(admin.ModelAdmin):
	pass

@admin.register(Gruppo)
class GruppoAdmin(admin.ModelAdmin):
	list_display = ['desiderio', 'utente_admin', 'punti']

@admin.register(PuntiGruppo)
class PuntiGruppoAdmin(admin.ModelAdmin):
	list_display = ['gruppo', 'utente', 'punti']

@admin.register(OrdineDesiderio)
class OrdineDesiderioAdmin(admin.ModelAdmin):
	list_display = ['gruppo', 'admin', 'timestamp', 'token', 'ritirato', 'partner_ritirato', 'timestamp_ritiro']

	def admin(self, obj):
		return obj.gruppo.utente_admin.email

@admin.register(PushNotification)
class PushNotificationAdmin(admin.ModelAdmin):
	list_display = ['utente', 'sistema_operativo', 'token']
	actions = [test_push]


