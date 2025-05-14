from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from orders.models import Order

class OrderAPITest(APITestCase):
    """
    Test case for the Order API endpoints
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
        
        # Create test order
        self.order = Order.objects.create(
            phone_number="+6281234567890",
            name="Test User",
            address="123 Test Street",
            total_lontong_large=2,
            total_lontong_small=3
        )
        
        # API endpoints
        self.list_url = reverse('order-list')
        self.detail_url = reverse('order-detail', args=[self.order.id])
        self.whatsapp_url = reverse('order-send-whatsapp', args=[self.order.id])
    
    def test_create_order_unauthenticated(self):
        """
        Test that an unauthenticated user can create an order
        """
        data = {
            'phone_number': '+6289876543210',
            'name': 'New User',
            'address': '456 New Street',
            'total_lontong_large': 1,
            'total_lontong_small': 2
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(name='New User').phone_number, '+6289876543210')
    
    def test_list_orders_unauthenticated(self):
        """
        Test that an unauthenticated user cannot list orders
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_orders_regular_user(self):
        """
        Test that a regular user cannot list orders
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_orders_admin(self):
        """
        Test that an admin user can list orders
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_retrieve_order_admin(self):
        """
        Test that an admin user can retrieve an order
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test User')
    
    def test_update_order_admin(self):
        """
        Test that an admin user can update an order
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'Updated User',
            'address': 'Updated Address'
        }
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated User')
        self.assertEqual(response.data['address'], 'Updated Address')
    
    def test_delete_order_admin(self):
        """
        Test that an admin user can delete an order
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
    
    def test_whatsapp_link_admin(self):
        """
        Test that an admin user can generate a WhatsApp link
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.whatsapp_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('whatsapp_link', response.data)
        self.assertTrue(response.data['whatsapp_link'].startswith('https://wa.me/'))