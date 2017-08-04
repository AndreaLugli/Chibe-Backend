from django.conf.urls import url
from .views import azienda_index
from .views import azienda_login
from .views import azienda_categorie
from .views import azienda_pagamento

urlpatterns = [
	url(r'^$', azienda_index, name = "azienda_index"),
	url(r'^login/', azienda_login.as_view(), name = "azienda_login"),
	url(r'^categorie/', azienda_categorie.as_view(), name = "azienda_categorie"),
	url(r'^pagamento/', azienda_pagamento.as_view(), name = "azienda_pagamento"),
]