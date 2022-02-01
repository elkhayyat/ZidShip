from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Courier(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Courier Name'))
    allow_to_cancel = models.BooleanField(
        default=False, verbose_name=_('Can Cancel?'))

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    name = models.CharField(verbose_name=_('Status Name'), max_length=128)

    def __str__(self):
        return self.name


class CourierStatus(models.Model):
    '''
    Used for Dynamic Status Mapping
    '''
    courier = models.ForeignKey(Courier, verbose_name=_('Courier'), on_delete=models.SET_NULL, null=True)
    courier_status = models.CharField(
        max_length=128, verbose_name=_('Courier Staus'))
    local_status = models.ForeignKey(
        OrderStatus, verbose_name=_('Local Status'), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.courier_status


class Order(models.Model):
    merchant = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('merchant'))
    courier = models.ForeignKey(
        Courier, on_delete=models.SET_NULL, null=True, verbose_name=_('Courier'))
    merchant_reference_id = models.CharField(
        max_length=128, verbose_name=_('Merchant Reference ID'), null=True, blank=True)
    courier_reference_id = models.CharField(
        max_length=128, verbose_name=_('Courier Reference ID'), null=True, blank=True)
    pickup_name = models.CharField(max_length=128, verbose_name=_('Sender Name'))
    pickup_phone_number = models.CharField(max_length=128, verbose_name=_('Sender Phone Number'))
    pickup_address = models.TextField(verbose_name=_('Pickup address'))

    dropoff_name = models.CharField(max_length=128, verbose_name=_('Receiver Name'))
    dropoff_phone_number = models.CharField(max_length=128, verbose_name=_('Receiver Phone Number'))
    dropoff_address = models.TextField(verbose_name=_('Drop Off Address'))
    
    order_status = models.ForeignKey(
        OrderStatus, on_delete=models.SET_NULL, null=True, blank=True)
    canceled = models.BooleanField(default=False, verbose_name=_('Canceled'))
    
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
