from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class AuthenticationTest(APITestCase):
    """
    Test case for authentication
    """
    def setUp(self):
        """
        Set up test data and users
        """
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        
        # Create regular user
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpassword'
        )
        
        # API endpoints
        self.token_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')
        self.orders_url = reverse('order-list')
    
    def test_obtain_token_admin(self):
        """
        Test that an admin user can obtain a JWT token
        """
        data = {
            'username': 'admin',
            'password': 'adminpassword'
        }
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_obtain_token_regular_user(self):
        """
        Test that a regular user can obtain a JWT token
        """
        data = {
            'username': 'user',
            'password': 'userpassword'
        }
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_refresh_token(self):
        """
        Test that a refresh token can be used to obtain a new access token
        """
        # First, obtain a token
        data = {
            'username': 'admin',
            'password': 'adminpassword'
        }
        response = self.client.post(self.token_url, data, format='json')
        refresh_token = response.data['refresh']
        
        # Then, use the refresh token to get a new access token
        data = {
            'refresh': refresh_token
        }
        response = self.client.post(self.token_refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_invalid_token(self):
        """
        Test that an invalid token is rejected
        """
        # Set an invalid token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid-token')
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_missing_token(self):
        """
        Test that a missing token is rejected
        """
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)