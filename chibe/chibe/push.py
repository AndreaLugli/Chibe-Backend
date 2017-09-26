# -*- coding: utf-8 -*-
from chibe.tasks import send_push_gcm, send_push_apns
from main.models import PushNotification
from django.conf import settings

IS_LOCAL = settings.IS_DEBUG

def push_generic(member, content):
	send_push(member, content)

def send_push(member, content):
	all_push = PushNotification.objects.filter(utente = member) 
	for push in all_push:
		o_system = push.sistema_operativo
		token = push.token

		if o_system == "Android":
			if IS_LOCAL:
				send_push_gcm(token, content)
			else:
				send_push_gcm.delay(token, content)
		else:
			if IS_LOCAL:
				send_push_apns(token, content, IS_LOCAL)
			else:
				send_push_apns.delay(token, content, IS_LOCAL)