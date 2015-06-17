from django import forms
from django.contrib.auth.models import User
from videochat.models import Chat

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('first_name','last_name','username','email','password')

class ChatForm(forms.ModelForm):
	class Meta:
		model = Chat
		fields = ('contact',)