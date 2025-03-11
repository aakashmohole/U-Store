import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)  # ✅ Logging for debugging

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        logger.info("🔍 Checking for access token in cookies...")  # ✅ Check if function is called

        token = request.COOKIES.get("access_token")  # ✅ Get token from cookies
        logger.info(f"📝 Found Token: {token}")  # ✅ Log token value

        if not token:
            logger.error("❌ No access token found")
            return None

        try:
            validated_token = self.get_validated_token(token)  # ✅ Decode token
            user = self.get_user(validated_token)  # ✅ Get user from token
            logger.info(f"✅ Authenticated User: {user}")
            return (user, validated_token)  # ✅ Correct return format
        except Exception as e:
            logger.error(f"❌ Authentication failed: {e}")  # ✅ Debugging
            raise AuthenticationFailed("Invalid or expired token")
