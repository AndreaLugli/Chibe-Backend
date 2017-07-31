from django.conf.urls import url
from .views import azienda_index
from .views import azienda_login

urlpatterns = [
	url(r'^$', azienda_index, name = "azienda_index"),
	url(r'^login/', azienda_login.as_view(), name = "azienda_login"),
]