from django.conf.urls import url
from .views import utente_register

urlpatterns = [
	url(r'^register/', utente_register.as_view(), name = "utente_register"),
]