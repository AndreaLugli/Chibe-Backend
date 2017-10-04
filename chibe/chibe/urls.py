from django.conf.urls import include, url
from django.contrib import admin

from main.views import utente_invito

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^azienda/', include('azienda.urls')), #Include from app azienda
    url(r'^utente/', include('main.urls')), #Include from app azienda
    url(r'^desideri/', include('desideri.urls')), #Include from app azienda
    url(r'^staff/', include('staff.urls')), #Include from app azienda
    url('', include('social_django.urls', namespace='social')),
    url(r'^invito/(?P<token>[\w-]+)/$', utente_invito.as_view(), name = "utente_invito"),
]
