# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.mail import EmailMessage
from celery import shared_task
from django.conf import settings
from gcm import GCM
from gobiko.apns import APNsClient
from main.models import PushNotification

PATH_CERT = settings.PATH_CERT
APNS_AUTH_KEY = PATH_CERT
APNS_KEY_ID = '4L273B4DB4'
TEAM_ID = 'SLD359N53R'
BUNDLE_ID = "it.socialcities.chibeb2c"

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

	try:
		gcm.plaintext_request(registration_id=token, data=data)
	except:
		PushNotification.objects.filter(token = token).delete()
		pass

@shared_task
def send_push_apns(token_hex, content, IS_LOCAL):
	client = APNsClient(
		team_id=TEAM_ID,
		bundle_id=BUNDLE_ID,
		auth_key_id=APNS_KEY_ID,
		auth_key_filepath=APNS_AUTH_KEY,
		use_sandbox=IS_LOCAL,
		force_proto='h2'
	)

	try:
		client.send_message(
			token_hex, 
			content,
			sound = "default"
		)
	except:
		PushNotification.objects.filter(token = token_hex).delete()
		pass










