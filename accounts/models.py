from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import EmailField
from accounts.managers import CustomUserManager
from rest_framework.authtoken.models import Token

# Create your models here.


class User(AbstractUser):
    '''
    creating custom model for user based on Abstract User to authenticate using email not username
    '''
    username = models.CharField(
        null=True, blank=True, unique=False, max_length=128)
    email = models.EmailField(unique=True, blank=False, null=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name:
            return self.get_full_name()
        else:
            return self.email
        
    @property
    def token(self):
        token = Token.objects.get(user=self)
        return token
