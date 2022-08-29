from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=150)
    message = models.CharField(max_length=2000)
    received_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    received_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
