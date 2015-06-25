from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.CharField(max_length=200)
    email = models.EmailField()
    user = models.ForeignKey(User, related_name="user")
    
class Chat(models.Model):
    chatname = models.CharField(max_length=100)
    chatstart = models.DateTimeField(default=timezone.now)
    chatend = models.DateTimeField(null=True)
    STATUS_CODES = (("Initialize","Initializing"),("Active","Active"),
	        ("Waiting","Waiting"),
	        ("Terminated","Terminated"))
    chat_status = models.CharField(max_length=10, choices=STATUS_CODES, default="Initialize")
    user = models.ForeignKey(User, null=True, related_name="chat")
    contact = models.ForeignKey(Contact, null=True, related_name="chat")


