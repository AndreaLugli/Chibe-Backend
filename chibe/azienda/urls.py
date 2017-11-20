from django.conf.urls import url
from .views import azienda_index
from .views import azienda_login
from .views import azienda_categorie
from .views import azienda_pagamento
from .views import azienda_search
from .views import azienda_id
from .views import azienda_premio
from .views import azienda_fornitore

from .views import test

urlpatterns = [
	url(r'^$', azienda_index, name = "azienda_index"),
	url(r'^login/', azienda_login.as_view(), name = "azienda_login"),
	url(r'^categorie/', azienda_categorie.as_view(), name = "azienda_categorie"),
	url(r'^pagamento/', azienda_pagamento.as_view(), name = "azienda_pagamento"),
	url(r'^premio/', azienda_premio.as_view(), name = "azienda_premio"),
	url(r'^fornitore/', azienda_fornitore.as_view(), name = "azienda_fornitore"),
	url(r'^search', azienda_search.as_view(), name = "azienda_search"),
	url(r'^(?P<id>[0-9]+)/', azienda_id.as_view(), name = "azienda_id"),
	url(r'^test/', test, name = "test"),
]