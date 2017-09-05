# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from chibe.tasks import send_email_task
from django.conf import settings

FROM = "chibe@chibeapp.com"
IS_LOCAL = settings.DEBUG

def email_reset_password(to, token):
	subject = "[CHIBE] Reset password"

	url = reverse('utente_forgot_password_token', kwargs = {'token': token})

	if IS_LOCAL:
		url = "http://127.0.0.1:8000" + url
	else:
		url = "http://app.chibeapp.com" + url
	
	message = "\
		Reimposta la password al seguente <a href='%s'>link</a>" % (url)

	if IS_LOCAL:
		send_email_task(subject, message, FROM, to)
	else:
		send_email_task.delay(subject, message, FROM, to)