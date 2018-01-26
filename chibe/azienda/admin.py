# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import Partner, Categoria, ContrattoMarketing, Acquisto, Fattura

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
	list_display = ['ragione_sociale', "email", "attivo", 'is_fornitore', "categoria_partner", "tribu", "orsi", "aquile", "lupi", "puma", "volpi"]
	fields = ["logo", "banner", "username", "contratto", "first_name", "last_name", "email", "attivo", "categoria_partner", "ragione_sociale", "codice_fiscale", "partita_iva", "indirizzo", "latitudine", "longitudine", "telefono_fisso", "telefono_cellulare", "descrizione", "categorie", "is_fornitore", "tribu", "orsi", "aquile", "lupi", "puma", "volpi"]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	pass

@admin.register(ContrattoMarketing)
class ContrattoMarketingAdmin(admin.ModelAdmin):
	list_display = ['etichetta', 'id', 'percentuale_marketing', 'inizio', 'fine', 'tacito_rinnovo', 'fatturazione', 'documentazione_traffico_acquisti', 'periodo_documentazione']

@admin.register(Acquisto)
class AcquistoAdmin(admin.ModelAdmin):
	list_display = ['utente', 'partner', 'importo', 'timestamp']

#@admin.register(Fattura)
class FatturaAdmin(admin.ModelAdmin):
	list_display = ["partner", "importo", "periodo_iniziale", "periodo_finale"]