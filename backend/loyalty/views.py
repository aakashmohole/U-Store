from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import LoyaltyPoints, LoyaltyTransaction
from .serializers import LoyaltyPointsSerializer, LoyaltyTransactionSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle
from authentication.views import CookieJWTAuthentication
from rest_framework.views import APIView
from rest_framework import status


class LoyaltyPointsRateLimit(UserRateThrottle):
    rate = '20/min' 


class LoyaltyPointsView(generics.RetrieveAPIView):
    
    serializer_class = LoyaltyPointsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    throttle_classes = [LoyaltyPointsRateLimit]
    
    def get_queryset(self):
        return LoyaltyPoints.objects.get_or_create(user=self.request.user)[0]
    
    
class LoyaltyTransactionListView(generics.ListAPIView):
    serializer_class = LoyaltyTransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    throttle_classes = [LoyaltyPointsRateLimit]

    def get_queryset(self):
        return LoyaltyTransaction.objects.filter(user=self.request.user)

class RedeemLoyaltyPointsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        points_to_redeem = request.data.get("points")

        if not points_to_redeem or float(points_to_redeem) <= 0:
            return Response({"error": "Invalid points amount"}, status=status.HTTP_400_BAD_REQUEST)

        loyalty_account, created = LoyaltyPoints.objects.get_or_create(user=user)

        if loyalty_account.points < float(points_to_redeem):
            return Response({"error": "Insufficient loyalty points"}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct points
        loyalty_account.points -= float(points_to_redeem)
        loyalty_account.save()

        # Record transaction
        LoyaltyTransaction.objects.create(user=user, points=float(points_to_redeem), transaction_type="Redeemed")

        return Response({"message": "Loyalty points redeemed successfully"}, status=status.HTTP_200_OK)
