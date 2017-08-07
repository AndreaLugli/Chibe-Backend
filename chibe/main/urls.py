from django.conf.urls import url

from .views import utente_register
from .views import utente_province
from .views import utente_step1, utente_step2, utente_step3

urlpatterns = [
	url(r'^register/', utente_register.as_view(), name = "utente_register"),
	url(r'^province/', utente_province.as_view(), name = "utente_province"),	
	url(r'^step1/', utente_step1.as_view(), name = "utente_step1"),
	url(r'^step2/', utente_step2.as_view(), name = "utente_step2"),	
	url(r'^step3/', utente_step3.as_view(), name = "utente_step3"),		
]