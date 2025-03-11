from django.shortcuts import render
import cloudinary.uploader
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.throttling import UserRateThrottle
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ProductFilter
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from authentication.views import CookieJWTAuthentication
from rest_framework.response import Response
# Custom throttle for sellers
class SellerRateThrottle(UserRateThrottle):
    rate = '20/min'  # Limit sellers to 10 requests per minute

# ✅ List & Create Products (Only Sellers/Admins can add products)
@authentication_classes([JWTAuthentication])
class ProductListCreateView(ListCreateAPIView):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    # authentication_classes = [CookieJWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [SellerRateThrottle]

    # # ✅ Enable filtering, searching, and sorting
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_class = ProductFilter  # Use the custom filter class
    # search_fields = ['name', 'description']  # Search by name or description
    # ordering_fields = ['price', 'created_at']  # Allow sorting by price & date
    

    # def get_queryset(self):
    #     cached_products = cache.get("all_products")
    #     if cached_products:
    #         return cached_products  # Return cached data

    #     products = Product.objects.all()
    #     cache.set("all_products", products, timeout=60*5)  # Cache for 5 mins
    #     return products

    # def perform_create(self, serializer):
    #     image = self.request.FILES.get('image', None)

    #     if image:
    #         upload_result = cloudinary.uploader.upload(image, folder="UStore_Products")
    #         serializer.save(image=upload_result['secure_url'])  # Save Cloudinary URL

    #     else:
    #         serializer.save()  # Save without an image
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()  # ✅ Fix: Use get_queryset

# ✅ Retrieve, Update, Delete a Product (Only Sellers/Admins)
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        image = self.request.FILES.get('image', None)

        if image:
            upload_result = cloudinary.uploader.upload(image, folder="UStore_Products")
            serializer.save(image=upload_result['secure_url'])  # Update with new image
        else:
            serializer.save()  # Update other fields only
