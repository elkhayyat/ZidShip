from dataclasses import field
from operator import mod
from rest_framework import serializers
from orders import models

class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Courier
        fields = '__all__'
        

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderStatus
        fields = '__all__'
    

class CourierOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourierStatus
        fields = '__all__'
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
