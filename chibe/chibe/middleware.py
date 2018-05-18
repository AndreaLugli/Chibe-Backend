from social_django.middleware import SocialAuthExceptionMiddleware
from social_core.exceptions import AuthForbidden
from django.http import HttpResponse

class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
	def process_exception(self, request, exception):
		return HttpResponse("Processo di registrazione cancellato")

class CheckAuth(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		user = request.user

		is_authenticated = user.is_authenticated()

		path = request.path

		if ("get_code" not in path) and ("session" not in path) and ("invito/successo" not in path) and ("google-plus" not in path) and ("admin" not in path) and ("staff" not in path) and ("desideri/new" not in path) and ("azienda/search" not in path) and ("azienda/login" not in path) and ("/invito/" not in path) and ("/utente/register-by-token" not in path) and ("/utente/register" not in path) and ("/utente/check_connected/" not in path) and ("/utente/login" not in path) and ("/utente/forgot-password" not in path):
			if is_authenticated:
				response = self.get_response(request)
				return response
			else:
				return HttpResponse('not_logged', status=401)
		else:		
			response = self.get_response(request)
		 	return response