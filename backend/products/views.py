from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ProductFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from authentication.views import CookieJWTAuthentication
import cloudinary.uploader

# ✅ Custom throttle for sellers
class SellerRateThrottle(UserRateThrottle):
    rate = '20/min'  # Limit sellers to 20 requests per minute

# ✅ Product List & Create (Sellers can add, Everyone can view)
class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]  # ✅ Only authenticated users (sellers/admins)
    throttle_classes = [SellerRateThrottle]  # ✅ Throttle only sellers

    # ✅ Filtering, Searching, and Sorting
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        """ ✅ Cache products for faster performance """
        cached_products = cache.get("all_products")
        if cached_products:
            return cached_products  

        products = Product.objects.all()
        cache.set("all_products", products, timeout=60*5)  # Cache for 5 minutes
        return products

    def perform_create(self, serializer):
        """ ✅ Only sellers (users) can create products, and images are uploaded to Cloudinary """
        user = self.request.user
        if user.user_type != 'User':  # 'User' = Seller
            return Response({"error": "Only sellers can add products"}, status=403)

        image = self.request.FILES.get('image', None)
        if image:
            upload_result = cloudinary.uploader.upload(image, folder="UStore_Products")
            serializer.save(image=upload_result['secure_url'], seller=user)
        else:
            serializer.save(seller=user)

# ✅ Retrieve, Update, Delete a Product (Only Admins)
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]  # ✅ Only admins (buyers) can manage products

    def perform_update(self, serializer):
        """ ✅ Only admins can update products, and images are uploaded to Cloudinary """
        user = self.request.user
        if user.user_type != 'Admin':  # 'Admin' = Buyer
            return Response({"error": "Only admins can update products"}, status=403)

        image = self.request.FILES.get('image', None)
        if image:
            upload_result = cloudinary.uploader.upload(image, folder="UStore_Products")
            serializer.save(image=upload_result['secure_url'])
        else:
            serializer.save()

    def perform_destroy(self, instance):
        """ ✅ Only admins can delete products """
        user = self.request.user
        if user.user_type != 'Admin':
            return Response({"error": "Only admins can delete products"}, status=403)
        instance.delete()
