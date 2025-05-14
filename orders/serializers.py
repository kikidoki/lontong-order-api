from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    whatsapp_link = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'phone_number', 'name', 'address',
            'total_lontong_large', 'total_lontong_small',
            'total_price', 'created_at', 'updated_at',
            'whatsapp_link'
        ]
        read_only_fields = ['id', 'total_price', 'created_at', 'updated_at', 'whatsapp_link']
    
    def get_whatsapp_link(self, obj):
        """
        Get the WhatsApp link for the order
        """
        return obj.get_whatsapp_link()