from django.conf.urls import url
from .views import azienda_index

urlpatterns = [
	url(r'^$', azienda_index, name = "azienda_index"),
]