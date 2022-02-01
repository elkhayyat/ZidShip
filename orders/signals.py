from sympy import im
from .models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import functions


@receiver(post_save, sender=Order)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    '''
    If it is a new order:
        make a request to courier API to create order
        after courier order creation
        
    '''
    if created:
        if instance.courier__id == 1:
            resp = requests.get('')
            
