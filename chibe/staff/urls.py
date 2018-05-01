from django.conf.urls import url
from .views import staff_index
from .views import staff_push

urlpatterns = [
	url(r'^$', staff_index.as_view(), name = "staff_index"),
	url(r'^push/$', staff_push.as_view(), name = "staff_push"),
]

