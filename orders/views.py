from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Order
from .serializers import OrderSerializer
from .permissions import IsAdminUser

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Order instances.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            # Allow anyone to create an order
            permission_classes = [AllowAny]
        else:
            # All other actions require admin privileges
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def send_whatsapp(self, request, pk=None):
        """
        Custom action to send WhatsApp message
        """
        order = self.get_object()
        whatsapp_link = order.get_whatsapp_link()
        return Response({
            'message': 'WhatsApp link generated successfully',
            'whatsapp_link': whatsapp_link
        })