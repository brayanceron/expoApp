from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):
    email=models.EmailField(('email addres'),unique=True)
    is_staff=models.BooleanField( default=True, )
    is_active=models.BooleanField(  default=True, )
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','password']
