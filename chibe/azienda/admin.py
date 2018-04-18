# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
import unicodecsv as csv
from .models import Partner, Categoria, ContrattoMarketing, Acquisto, Fattura
from django.http import HttpResponse

def export_partner(modeladmin, request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="Partner.csv"'

	writer = csv.writer(response)
	writer.writerow(['ragione_sociale', "email", "attivo", 'is_fornitore', "categoria_partner", "tribu", "orsi", "aquile", "lupi", "puma", "volpi"])

	for partner in queryset:
		ragione_sociale = partner.ragione_sociale
		email = partner.email
		attivo = partner.attivo
		is_fornitore = partner.is_fornitore
		categoria_partner = partner.categoria_partner
		tribu = partner.tribu
		orsi = partner.orsi
		aquile = partner.aquile
		lupi = partner.lupi
		puma = partner.puma
		volpi = partner.volpi

		writer.writerow([ragione_sociale, email, attivo, is_fornitore, categoria_partner, tribu, orsi, aquile, lupi, puma, volpi])

	return response

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
	list_display = ['ragione_sociale', 'ragione_sociale_fattura', "email", "attivo", 'is_fornitore', "categoria_partner", "tribu", "orsi", "aquile", "lupi", "puma", "volpi"]
	fields = ["logo", "banner", "username", "tripadvisor", "contratto", "first_name", "last_name", "email", "attivo", "categoria_partner", "ragione_sociale", "ragione_sociale_fattura", "codice_fiscale", "partita_iva", "indirizzo", "latitudine", "longitudine", "telefono_fisso", "telefono_cellulare", "descrizione", "categorie", "is_fornitore", "tribu", "orsi", "aquile", "lupi", "puma", "volpi"]
	actions = [export_partner]


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	pass


def export_contratto(modeladmin, request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="ContrattoMarketing.csv"'

	writer = csv.writer(response)
	writer.writerow(['etichetta', 'id', 'percentuale_marketing', 'inizio', 'fine', 'tacito_rinnovo', 'fatturazione', 'documentazione_traffico_acquisti', 'periodo_documentazione'])

	for contratto in queryset:
		etichetta = contratto.etichetta
		id = contratto.id
		percentuale_marketing = contratto.percentuale_marketing
		inizio = contratto.inizio
		fine = contratto.fine
		tacito_rinnovo = contratto.tacito_rinnovo
		fatturazione = contratto.fatturazione
		documentazione_traffico_acquisti = contratto.documentazione_traffico_acquisti
		periodo_documentazione = contratto.periodo_documentazione

		writer.writerow([etichetta, id, percentuale_marketing, inizio, fine, tacito_rinnovo, fatturazione, documentazione_traffico_acquisti, periodo_documentazione])

	return response


@admin.register(ContrattoMarketing)
class ContrattoMarketingAdmin(admin.ModelAdmin):
	list_display = ['etichetta', 'id', 'percentuale_marketing', 'inizio', 'fine', 'tacito_rinnovo', 'fatturazione', 'documentazione_traffico_acquisti', 'periodo_documentazione']
	actions = [export_contratto]


def export_acquisto(modeladmin, request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="Acquisti.csv"'

	writer = csv.writer(response)
	writer.writerow(['utente', 'partner', 'importo', 'timestamp'])

	for acq in queryset:
		utente = acq.utente.username
		partner = acq.partner.ragione_sociale
		importo = acq.importo
		timestamp = acq.timestamp

		writer.writerow([utente, partner, importo, timestamp])

	return response

@admin.register(Acquisto)
class AcquistoAdmin(admin.ModelAdmin):
	list_display = ['utente', 'partner', 'importo', 'timestamp']

	actions = [export_acquisto]







