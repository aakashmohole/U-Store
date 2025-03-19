from django.urls import path
from .views import LoyaltyPointsView, LoyaltyTransactionListView, RedeemLoyaltyPointsView

urlpatterns = [
    path('loyalty-points/', LoyaltyPointsView.as_view(), name='loyalty-points'),
    path('loyalty-transactions/', LoyaltyTransactionListView.as_view(), name='loyalty-transactions'),
    path('redeem-loyalty/', RedeemLoyaltyPointsView.as_view(), name='redeem-loyalty'),
]
