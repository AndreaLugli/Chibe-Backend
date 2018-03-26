# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.http import HttpResponse
import unicodecsv as csv
from .models import Desiderio, CategoriaDesiderio

@admin.register(CategoriaDesiderio)
class CategoriaDesiderioAdmin(admin.ModelAdmin):
	list_display = ['nome', 'id_immagine', 'descrizione']


def export_desiderio(modeladmin, request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="Desideri.csv"'

	writer = csv.writer(response)
	writer.writerow(['nome', 'descrizione_breve', 'punti_piuma', 'costo_riscatto', 'data_inizio', 'data_fine', 'num_gruppo', 'sku', 'in_evidenza'])

	for desiderio in queryset:
		nome = desiderio.nome
		descrizione_breve = desiderio.descrizione_breve
		punti_piuma = desiderio.punti_piuma
		costo_riscatto = desiderio.costo_riscatto
		data_inizio = desiderio.data_inizio
		data_fine = desiderio.data_fine
		num_gruppo = desiderio.num_gruppo
		sku = desiderio.sku
		in_evidenza = desiderio.in_evidenza

		writer.writerow([nome, descrizione_breve, punti_piuma, costo_riscatto, data_inizio, data_fine, num_gruppo, sku, in_evidenza])

	return response

@admin.register(Desiderio)
class DesiderioAdmin(admin.ModelAdmin):
	list_display = ['nome', 'descrizione_breve', 'punti_piuma', 'costo_riscatto', 'data_inizio', 'data_fine', 'num_gruppo', 'sku', 'in_evidenza']

	actions = [export_desiderio]