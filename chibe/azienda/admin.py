# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import Partner, Categoria, ContrattoMarketing

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
	fields = ["first_name", "last_name", "ragione_sociale", "codice_fiscale", "partita_iva", "username", "indirizzo", "latitudine", "longitudine", "telefono_fisso", "telefono_cellulare", "descrizione", "categorie", "is_fornitore", "famoco_id", "tribu"]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	pass

@admin.register(ContrattoMarketing)
class ContrattoMarketingAdmin(admin.ModelAdmin):
	pass