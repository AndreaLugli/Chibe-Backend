# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import Partner, Categoria

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
	fields = ["first_name", "last_name", "ragione_sociale", "username", "password", "indirizzo", "latitudine", "longitudine", "telefono_fisso", "telefono_cellulare", "descrizione", "categorie", "status", "is_fornitore", "famoco_id", "tribu"]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	pass