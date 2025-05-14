from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from orders.models import Order

class IntegrationTest(APITestCase):
    """
    Integration tests for the Order API
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
        
        # API endpoints
        self.token_url = reverse('token_obtain_pair')
        self.orders_url = reverse('order-list')
    
    def test_end_to_end_order_flow(self):
        """
        Test the complete order flow from creation to deletion
        """
        # 1. Create an order as an unauthenticated user
        order_data = {
            'phone_number': '+6281234567890',
            'name': 'Integration Test User',
            'address': '789 Integration Street',
            'total_lontong_large': 3,
            'total_lontong_small': 2
        }
        
        response = self.client.post(self.orders_url, order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order_id = response.data['id']
        
        # 2. Get a token for the admin user
        token_data = {
            'username': 'admin',
            'password': 'adminpassword'
        }
        response = self.client.post(self.token_url, token_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        
        # 3. Use the token to authenticate
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # 4. List all orders as admin
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # 5. Get the specific order
        detail_url = reverse('order-detail', args=[order_id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Integration Test User')
        
        # 6. Update the order
        update_data = {
            'address': 'Updated Integration Address'
        }
        response = self.client.patch(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['address'], 'Updated Integration Address')
        
        # 7. Generate WhatsApp link
        whatsapp_url = reverse('order-send-whatsapp', args=[order_id])
        response = self.client.post(whatsapp_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('whatsapp_link', response.data)
        
        # 8. Delete the order
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # 9. Verify the order is deleted
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)