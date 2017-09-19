# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.mail import EmailMessage
from celery import shared_task

from apns import APNs, Payload
from gcm import GCM
PATH_CERT = "settings.PATH_CERT"

@shared_task
def send_email_task(subject, message, FROM, to):
	msg = EmailMessage(subject, message, FROM, [to])
	msg.content_subtype = "html"
	msg.send()

@shared_task
def send_push_gcm(token, content):
	google_api_key = "AAAAgGY9xAc:APA91bFwKXq9w7sB6EKzNGvIKInrc8VF8TRu3SInUM1zbisRmSX9gnlMcWFam4uIMoeAv0CGhNlwrEHvEI7htSbg6-2YHQ2hIgD0agKF95GZ_tEduz4pTDSJiQj2tpZ10hGPPLapIEvm"

	gcm = GCM(google_api_key)
	data = {'message': content, 'title' : 'Chibe'}

	gcm.plaintext_request(registration_id=token, data=data)

@shared_task
def send_push_apns(token, content, IS_LOCAL):
	if IS_LOCAL:
		use_sandbox = True		
	else:
		use_sandbox = False

	apns = APNs(use_sandbox=use_sandbox, cert_file=PATH_CERT, key_file=PATH_CERT)
	payload = Payload(alert = content, sound="default", badge = 1)
	
	apns.gateway_server.send_notification(token, payload)