from django.conf.urls import url

from .views import desideri_home, desideri_new_home
from .views import desideri_id

urlpatterns = [
	url(r'^$', desideri_home, name = 'desideri_home'),
	url(r'^new/$', desideri_new_home, name = 'desideri_new_home'),
	url(r'^(?P<id>[0-9]+)/', desideri_id.as_view(), name = "desideri_id"),
]

