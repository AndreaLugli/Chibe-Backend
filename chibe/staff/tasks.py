# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from main.models import Utente
from chibe.push import push_generic

@shared_task
def send_all_push(testo):
	utenti = Utente.objects.all()
	for member in utenti:
		push_generic(member, testo)