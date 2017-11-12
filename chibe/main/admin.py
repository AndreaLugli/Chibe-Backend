# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import Utente, OnBoard, Provincia, Scuola, Tribu, Gruppo, PushNotification, PuntiGruppo, OrdineDesiderio
from chibe.tasks import send_push_gcm, send_push_apns

def test_push(modeladmin, request, queryset):
	content = "Test"
	for push in queryset:
		o_system = push.sistema_operativo
		token = push.token

		if o_system == "Android":
			send_push_gcm(token, content)
		else:
			send_push_apns(token, content, True)

@admin.register(Utente)
class UtenteAdmin(admin.ModelAdmin):
	list_display = ['username', 'tribu', 'punti', 'avatar', 'codice', 'email', 'first_name', 'last_name', 'telefono_cellulare', 'provincia', 'scuola', 'classe', 'sesso', 'compleanno', 'invite_link']
	fields = ('username', 'first_name', 'last_name', 'email', 'avatar', 'classe', 'telefono_cellulare', 'descrizione', 'status', 'codice', 'punti', 'provincia', 'scuola', 'tribu', 'tribu_timestamp', 'amici', 'sesso', 'compleanno')

@admin.register(OnBoard)
class OnBoardAdmin(admin.ModelAdmin):
	list_display = ['utente', 'step_1', 'step_2', 'step_3', 'complete', 'fb_step_1', 'fb_step_2', 'fb_complete']

@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
	pass

@admin.register(Scuola)
class ScuolaAdmin(admin.ModelAdmin):
	pass

@admin.register(Tribu)
class TribuAdmin(admin.ModelAdmin):
	pass

@admin.register(Gruppo)
class GruppoAdmin(admin.ModelAdmin):
	list_display = ['desiderio', 'utente_admin', 'punti']

@admin.register(PuntiGruppo)
class PuntiGruppoAdmin(admin.ModelAdmin):
	pass

@admin.register(OrdineDesiderio)
class OrdineDesiderioAdmin(admin.ModelAdmin):
	pass

@admin.register(PushNotification)
class PushNotificationAdmin(admin.ModelAdmin):
	list_display = ['utente', 'sistema_operativo', 'token']
	actions = [test_push]


