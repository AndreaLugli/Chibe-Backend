from django.conf.urls import url
from .views import staff_index

urlpatterns = [
	url(r'^', staff_index.as_view(), name = "staff_index"),
]

