from django import forms
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class NameForm(forms.Form):
	email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
	password_1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}))
	password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}))
	username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
	captcha = ReCaptchaField(widget=ReCaptchaWidget())

