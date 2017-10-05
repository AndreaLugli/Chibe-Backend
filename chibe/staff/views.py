# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.shortcuts import render
from django.contrib import messages

from azienda.models import Partner

class staff_index(View):
	def dispatch(self, *args, **kwargs):
		return super(staff_index, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):

		template_name = "staff_index.html"
		return render(request, template_name)

	def post(self, request, *args, **kwargs):

		piva = request.POST.get("piva", "")
		codice = request.POST.get("codice", "")

		if codice == "ciao":
			p_ex = Partner.objects.filter(partita_iva = piva).exists()

			if p_ex:
				partner = Partner.objects.get(partita_iva = piva)
				partner.attivo = False
				partner.save()

				messages.success(request, "Partner bloccato con successo")
			else:
				messages.error(request, "Il partner non esiste")
		else:
			messages.error(request, "Codice errato")
			
		url = reverse('staff_index')
		return HttpResponseRedirect(url)

