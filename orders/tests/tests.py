from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from orders.models import Courier

# Create your tests here.


class CourierViewSetTestCase(APITestCase):
    list_url = reverse('orders:Courier-list')

    def setUp(self) -> None:
        courier_name = 'Coruier1'
        courier = Courier.objects.create(name=courier_name)
        user_data = {
            'email': 'user@elkhayyat.me',
            'password': 'P@$$w0rd!',
        }
        self.user = get_user_model().objects.create_user(
            email=user_data['email'], password=user_data['password'])
        self.token = self.user.token
        self.api_authenticate()

    def api_authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))

    def test_string(self):
        courier_name = 'Coruier1'
        courier = Courier.objects.get(id=1)
        self.assertEqual(courier.__str__(), courier_name)

    def test_list_courier_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_courier_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


'''
ToDo: write Order ViewSet Test Case
'''

'''
ToDo: write OrderStatus ViewSet Test Case
'''

'''
ToDo: write CourierStatusViewSet Test Case
'''

'''
ToDo: write OrderStatuViewSet Test Case
'''

'''
ToDo: write OrderStatus view Test Case
'''
