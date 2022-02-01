from django.shortcuts import render
from rest_framework import viewsets, generics
from orders.models import Courier, OrderStatus, CourierStatus, Order
from orders import serializers
from rest_framework import permissions, response, status

# Create your views here.


class CourierViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourierSerializer

    def get_queryset(self):
        '''
        Query all Couriers Available
        '''
        queryset = Courier.objects.all()
        '''
        Filtering queryset using "GET" parameters
        ===============================
        id: <int> refer to courier ID
        name: <string> by parts of courier name
        '''
        courier_id = self.request.query_params.get('id')
        name = self.request.query_params.get('name')
        if courier_id:
            queryset = queryset.filter(id=courier_id)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class OrderStatusViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderStatusSerializer

    def get_queryset(self):
        '''
        Get all OrderStatus 
        '''
        queryset = OrderStatus.objects.all()
        '''
        Filtering OrderStatus using "GET" parameters
        ===============================
        id: <int> refer to order status ID
        name: <string> by parts of order status name
        '''
        status_id = self.request.query_params.get('status_id')
        name = self.request.query_params.get('name')
        if status_id:
            queryset = queryset.filter(id=status_id)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class CourierOrderStatusViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourierOrderStatusSerializer

    def get_queryset(self):
        '''
        Query all Courier Status
        '''
        queryset = CourierStatus.objects.all()
        '''
        Filter Courier Status using "GET" parameters
        ===============================
        courier_id: <int> refer to order id
        courier_status: <string> refer to courier status name
        local_status_id: <int> refer to the local status object id
        '''
        courier_id = self.request.query_params.get('courier_id')
        courier_status = self.request.query_params.get('courier_status')
        local_status_id = self.request.query_params.get('local_status_id')
        if courier_id:
            queryset = queryset.filter(id=courier_id)
        if courier_status:
            queryset = queryset.filter(
                courier_status__icontains=courier_status)
        if local_status_id:
            queryset = queryset.filter(local_status__id=local_status_id)
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        '''
        Query all orders
        '''
        queryset = Order.objects.all()
        '''
        Filter orders using "GET" parameters
        ===============================
        merchant_id: <int> refer to merchant id
        courier_id: <int> refer to courier id
        merchant_reference_id: <string> refer to order reference id at merchant database
        courier_reference_id: <sting> refer to courier order id
        order_status_id: <int> refer to order status id
        canceled: <bool> if 1 order is cancelled if 0 order is not canceled
        '''
        merchant_id = self.request.query_params.get('merchant_id')
        courier_id = self.request.query_params.get('courier_id')
        merchant_reference_id = self.request.query_params.get(
            'merchant_reference_id')
        courier_reference_id = self.request.query_params.get(
            'courier_reference_id')

        pickup_name = self.request.query_params.get('pickup_name')
        pickup_phone_number = self.request.query_params.get(
            'pickup_phone_number')
        pickup_address = self.request.query_params.get('pickup_address')

        dropoff_name = self.request.query_params.get('dropoff_name')
        dropoff_phone_number = self.request.query_params.get(
            'dropoff_phone_number')
        dropoff_address = self.request.query_params.get('dropoff_address')

        order_status_id = self.request.query_params.get('order_status_id')
        canceled = self.request.query_params.get('canceled')

        if merchant_id:
            queryset = queryset.filter(merchant__id=merchant_id)

        if courier_id:
            queryset = queryset.filter(courier__id=courier_id)

        if merchant_reference_id:
            queryset = queryset.filter(
                merchant_reference_id=merchant_reference_id)

        if courier_reference_id:
            queryset = queryset.filter(
                courier_reference_id=courier_reference_id)

        if pickup_name:
            queryset = queryset.filter(pickup_name__icontains=pickup_name)

        if pickup_phone_number:
            queryset = queryset.filter(
                pickup_phone_number__icontains=pickup_phone_number)

        if pickup_address:
            queryset = queryset.filter(
                pickup_address__icontains=pickup_address)

        if dropoff_name:
            queryset = queryset.filter(dropoff_name__icontains=dropoff_name)

        if dropoff_phone_number:
            queryset = queryset.filter(
                dropoff_phone_number__icontains=dropoff_phone_number)

        if dropoff_address:
            queryset = queryset.filter(
                dropoff_address__icontains=dropoff_address)

        if order_status_id:
            queryset = queryset.filter(order_status__id=order_status_id)

        if canceled == 1:
            queryset = queryset.filter(canceled=True)
        elif canceled == 0:
            queryset = queryset.filter(canceled=False)

        return queryset


class OrderStatus(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        if order.courier.id == 1:
            '''
            ToDo: 
            Make request to Courier API to get the current state
            '''

            '''
            ToDo:
            Map the the courier status to local status using "get_order_status_from_courier_status" function
            '''

            '''
            ToDo:
            Update the status of the order object to the new status
            '''

            '''
            ToDo:
            Return the order status
            '''

        else:
            '''
            return error
            '''
            response.Response({'message': 'can\'t find courier integration'},
                              status_code=status.HTTP_400_BAD_REQUEST)
