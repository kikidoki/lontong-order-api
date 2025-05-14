from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class Order(models.Model):
    """
    Order model for lontong business
    """
    # Phone number validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+628..'. Up to 15 digits allowed."
    )
    
    # Customer information
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    name = models.CharField(max_length=255)
    address = models.TextField()
    
    # Order details
    total_lontong_large = models.PositiveIntegerField(default=0)
    total_lontong_small = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculate total price based on quantities and prices
        large_price = settings.LONTONG_LARGE_PRICE * self.total_lontong_large
        small_price = settings.LONTONG_SMALL_PRICE * self.total_lontong_small
        self.total_price = large_price + small_price
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.id} - {self.name}"
    
    def get_whatsapp_link(self):
        """
        Generate WhatsApp link with order information
        """
        # Format phone number for WhatsApp (remove '+' if present)
        wa_phone = self.phone_number.lstrip('+')
        
        # Create order summary message
        message = (
            f"Hello {self.name}, "
            f"thank you for your order!\n\n"
            f"Order Summary:\n"
            f"- Large Lontong: {self.total_lontong_large} x {settings.LONTONG_LARGE_PRICE} IDR\n"
            f"- Small Lontong: {self.total_lontong_small} x {settings.LONTONG_SMALL_PRICE} IDR\n"
            f"Total: {self.total_price} IDR\n\n"
            f"Customer Address: {self.address}\n\n"
            f"We will process your order and inform you once it's ready for pickup."
            f"\n\nThank you for choosing us!"
        )
        
        # URL encode the message
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        
        # Return the WhatsApp link
        return f"https://wa.me/{wa_phone}?text={encoded_message}"
    
    class Meta:
        ordering = ['-created_at']