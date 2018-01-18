from social_django.middleware import SocialAuthExceptionMiddleware
from social_core.exceptions import AuthForbidden
from django.http import HttpResponse

class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
	def process_exception(self, request, exception):
		return HttpResponse("Processo di registrazione cancellato")