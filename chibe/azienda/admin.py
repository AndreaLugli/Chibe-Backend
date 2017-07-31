# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import Esercente

@admin.register(Esercente)
class EsercenteAdmin(admin.ModelAdmin):
	fields = ["ragione_sociale", "username", "password"]
