from django.test import TestCase
from django.conf import settings
from orders.models import Order

class OrderModelTest(TestCase):
    """
    Test case for the Order model
    """
    def setUp(self):
        """
        Set up test data
        """
        self.order = Order.objects.create(
            phone_number="+6281234567890",
            name="Test User",
            address="123 Test Street",
            total_lontong_large=2,
            total_lontong_small=3
        )
    
    def test_order_creation(self):
        """
        Test that an order can be created
        """
        self.assertEqual(self.order.name, "Test User")
        self.assertEqual(self.order.phone_number, "+6281234567890")
        self.assertEqual(self.order.address, "123 Test Street")
        self.assertEqual(self.order.total_lontong_large, 2)
        self.assertEqual(self.order.total_lontong_small, 3)
    
    def test_total_price_calculation(self):
        """
        Test that total price is calculated correctly
        """
        expected_price = (
            settings.LONTONG_LARGE_PRICE * self.order.total_lontong_large +
            settings.LONTONG_SMALL_PRICE * self.order.total_lontong_small
        )
        self.assertEqual(float(self.order.total_price), expected_price)
    
    def test_string_representation(self):
        """
        Test the string representation of an order
        """
        self.assertEqual(str(self.order), f"Order {self.order.id} - Test User")
    
    def test_whatsapp_link_generation(self):
        """
        Test that WhatsApp link is generated correctly
        """
        wa_link = self.order.get_whatsapp_link()
        
        # Check that the link starts with the correct URL
        self.assertTrue(wa_link.startswith("https://wa.me/6281234567890?text="))
        
        # Check that the link contains the order information
        self.assertIn("Test%20User", wa_link)
        self.assertIn("Large%20Lontong%3A%202", wa_link)
        self.assertIn("Small%20Lontong%3A%203", wa_link)