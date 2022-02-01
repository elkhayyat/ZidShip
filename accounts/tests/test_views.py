from tokenize import Token
from urllib import response
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts import models
from rest_framework.authtoken.models import Token


class UserTestCase(APITestCase):
    '''
    setting API endpoints URLs
    '''
    login_url = reverse('accounts:login')
    register_url = reverse('accounts:register')

    def test_registeration(self):
        '''
        Test register a new user endpoint
        '''
        data = {
            'email': 'test@elkhayyat.me',
            'password': 'P@$$w0rd!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicated_email(self):
        '''
        Test if trying to multiple registeration with the same email
        '''
        data = {
            'email': 'test@elkhayyat.me',
            'password': 'P@$$w0rd!',
        }
        response = self.client.post(self.register_url, data)
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        '''
        Test login API endpoint
        '''
        data = {
            'username': 'test@elkhayyat.me',
            'password': 'P@$$w0rd!',
        }
        self.user = models.User.objects.create_user(
            email=data['username'], password=data['password'])
        response = self.client.post('/api/accounts/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewSetTestCase(APITestCase):
    list_url = reverse('accounts:user-list')
    detail_url = reverse('accounts:user-detail', kwargs={'pk': 1})
    

    def setUp(self) -> None:
        '''
        Creating two accounts:
        1- User Account.
        2- Admin Account.
        '''
        self.user = models.User.objects.create_user(
            email='user@elkhayyat.me', password='P@$$w0rd!')
        self.user_token = models.Token.objects.get(user=self.user)
        self.admin = models.User.objects.create_superuser(
            email='admin@elkhayyat.me', password='P@$$w0rd!')
        self.admin_token = models.Token.objects.get(user=self.admin)

    def user_api_authenticate(self):
        '''
        Authenticate using User Account
        '''
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(self.user_token))

    def admin_api_authenticate(self):
        '''
        Authenticate using Admin Account
        '''
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(self.admin_token))

    def test_user_list_user_authenticated(self):
        '''
        Test authenticated user account
        It should return HTTP_403_FORBIDDEN because the permission is set to IsAdminOnly
        '''
        self.user_api_authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list_un_authenticated(self):
        '''
        Test unauthenticated request
        It should return HTTP_401_UNAUTHORIZED because can't use it without logging in
        '''
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_admin_authenticated(self):
        '''
        Test authenticated admin account.
        It should Works!
        '''
        self.admin_api_authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_creation(self):
        '''
        Test User creation using UserViewSet
        '''
        data = {
            'first_name': 'FName',
            'last_name': 'FName',
            'email': 'test@elkhayyat.me',
            'password': 'P@$$w0rd!'
        }
        self.admin_api_authenticate()
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        

    def test_user_update(self):
        '''
        Test User Update using UserViewSet
        '''
        data = {
            'first_name': 'fName',
            'last_name': 'lName',
            'email': 'user1@elkhayyat.me',
            'password': 'P@$$w0rd!'
        }
        self.admin_api_authenticate()
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], data['first_name'])