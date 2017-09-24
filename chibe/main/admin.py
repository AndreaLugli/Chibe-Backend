# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import Utente, OnBoard, Provincia, Scuola, Tribu, Gruppo, PushNotification

@admin.register(Utente)
class UtenteAdmin(admin.ModelAdmin):
	list_display = ['username', 'tribu', 'punti', 'avatar', 'codice', 'email', 'first_name', 'last_name', 'telefono_cellulare', 'provincia', 'scuola', 'classe', 'invite_link']

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

@admin.register(PushNotification)
class PushNotificationAdmin(admin.ModelAdmin):
	list_display = ['utente', 'sistema_operativo', 'token']

