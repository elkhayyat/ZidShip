import imp
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders import views



app_name = 'orders'
router = DefaultRouter()
router.register(r'couriers', views.CourierViewSet, basename='Courier')
router.register(r'order_status', views.OrderStatusViewSet, basename='OrderStatus')
router.register(r'courier_status', views.CourierOrderStatusViewSet, basename='CourierStatus')
router.register(r'orders', views.OrderViewSet, basename='Order')


urlpatterns = [
    path('', include(router.urls)),
    path('order-status/<int:pk>/', views.OrderStatus.as_view(), name='order-status'),
]

