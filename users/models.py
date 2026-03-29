from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# User -> patiant 
# User -> doctor 
# User -> Admin


class User(AbstractUser):
    
    class Gender (models.TextChoices):
        Male = 'male' , 'Male'
        Female = 'female' , 'Female'
    class Status (models.TextChoices):
        Active = 'active' , 'Active'
        Deactive = 'deactive' , 'Deactive'

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15 , blank=True , null=True)
    birth_date = models.DateField(blank=True , null=True)

    gender = models.CharField(max_length=100 , choices=  Gender.choices , null= True , blank=True)
    status = models.CharField(max_length=100 , choices= Status.choices , default=Status.Active)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class notes(models.Model):
    Author = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)