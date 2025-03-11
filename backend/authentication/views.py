from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Users
from .serializers import( RegisterSerializer, UserSerializer, LoginSerializer,
                         PasswordResetSerializer)
from rest_framework.throttling import UserRateThrottle
from .auth import CookieJWTAuthentication
class CustomThrottle(UserRateThrottle):
    rate = '5/min'  # Allow only 5 requests per minute

class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    throttle_classes = [CustomThrottle]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)

            # Set JWT token in HttpOnly cookie
            response.set_cookie(key="access_token", value=str(refresh.access_token), httponly=True)
            response.set_cookie(key="refresh_token", value=str(refresh), httponly=True)

            return response
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
# class CookieJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         token = request.COOKIES.get("access_token")  # ✅ Get token from cookies
#         if not token:
#             print("❌ No access token found in cookies")  # ✅ Debugging
#             return None  # ✅ Must return None if no token found

#         try:
#             validated_token = self.get_validated_token(token)  # ✅ Decode token
#             user = self.get_user(validated_token)  # ✅ Get user from token
#             return (user, validated_token)  # ✅ Corrected return format
#         except Exception as e:
#             print(f"❌ Authentication failed: {e}")  # ✅ Debugging
#             raise AuthenticationFailed("Invalid or expired token")  # ✅ Correct error message
        
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]  # Use custom authentication
    throttle_classes = [CustomThrottle]

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
#reset password view
class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)