from django.conf.urls import url

from .views import check_connected
from .views import utente_register, utente_login
from .views import utente_province, utente_province_id
from .views import utente_step1, utente_step2, utente_step3

urlpatterns = [
	url(r'^check_connected/$', check_connected, name = 'check_connected'),
	url(r'^login/', utente_login.as_view(), name = "utente_login"),
	url(r'^register/', utente_register.as_view(), name = "utente_register"),
	url(r'^province/$', utente_province.as_view(), name = "utente_province"),
	url(r'^province/(?P<id>[0-9]+)/$', utente_province_id.as_view(), name = "utente_province_id"),	
	url(r'^step1/', utente_step1.as_view(), name = "utente_step1"),
	url(r'^step2/', utente_step2.as_view(), name = "utente_step2"),	
	url(r'^step3/', utente_step3.as_view(), name = "utente_step3"),		
]