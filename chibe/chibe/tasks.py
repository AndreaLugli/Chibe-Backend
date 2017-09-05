# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.core.mail import EmailMessage
from celery import shared_task

@shared_task
def send_email_task(subject, message, FROM, to):
	msg = EmailMessage(subject, message, FROM, [to])
	msg.content_subtype = "html"
	msg.send()
