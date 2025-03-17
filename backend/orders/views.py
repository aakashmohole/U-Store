from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle
from authentication.views import CookieJWTAuthentication
# Create your views here.

class OrderRateLimit(UserRateThrottle):
    rate = '20/min' 


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class =  OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    throttle_classes = [OrderRateLimit]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class OrderDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    throttle_classes = [OrderRateLimit]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Order.objects.all()
    
class UpdateOrderStatusView(APIView):
    
    permission_classes = [IsAdminUser]
    authentication_classes = [CookieJWTAuthentication]
    throttle_classes = [OrderRateLimit]
    
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id = order_id)
            new_status = request.data.get('status')
            
            if new_status in [choice[0] for choice in Order.STATUS_CHOICES]:
                order.status = new_status
                order.save()
                return Response({'message': 'Order status updated successfully'}, status=200)
            return Response({'error' : 'Invalid status'}, status=400)
        except order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)