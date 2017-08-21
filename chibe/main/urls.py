from django.conf.urls import url

from .views import check_connected
from .views import utente_register, utente_login
from .views import utente_province, utente_province_id
from .views import utente_step1, utente_step2, utente_step3
from .views import upload_picture
from .views import get_code
from .views import search_amico
from .views import utente_amici
from .views import utente_amico_add, utente_amico_delete
from .views import utente_info
from .views import utente_tribu
from .views import utente_modifica
from .views import utente_desideri

urlpatterns = [
	url(r'^check_connected/$', check_connected, name = 'check_connected'),
	url(r'^upload_picture/$', upload_picture, name = 'upload_picture'),
	url(r'^login/', utente_login.as_view(), name = "utente_login"),
	url(r'^register/', utente_register.as_view(), name = "utente_register"),
	url(r'^province/$', utente_province.as_view(), name = "utente_province"),
	url(r'^province/(?P<id>[0-9]+)/$', utente_province_id.as_view(), name = "utente_province_id"),	
	url(r'^step1/', utente_step1.as_view(), name = "utente_step1"),
	url(r'^step2/', utente_step2.as_view(), name = "utente_step2"),	
	url(r'^step3/', utente_step3.as_view(), name = "utente_step3"),	
	url(r'^get_code/$', get_code, name = 'get_code'),	
	url(r'^search_amico/$', search_amico, name = 'search_amico'),	
	url(r'^amici/$', utente_amici, name = 'amici'),	
	url(r'^amico/add/$', utente_amico_add, name = 'utente_amico_add'),	
	url(r'^amico/delete/$', utente_amico_delete, name = 'utente_amico_delete'),	
	url(r'^info/$', utente_info, name = 'utente_info'),	
	url(r'^tribu/$', utente_tribu, name = 'utente_tribu'),	
	url(r'^modifica/$', utente_modifica, name = 'utente_modifica'),	
	url(r'^desideri/$', utente_desideri, name = 'utente_desideri'),	
]

