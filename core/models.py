from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class CustomInformationUser(AbstractUser):
    address= models.TextField(null=True,blank=True)
    city= models.CharField(max_length=150,null=True,blank=True)
    phone = PhoneNumberField(unique=True,blank=True,)
    avatar = models.ImageField(upload_to='user',null=True,blank=True,default='user/happystick.jpg')
    def __str__(self):
        return self.username
    