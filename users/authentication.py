from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # 1. Проверяем токен в cookies (для HTTP-only)
        raw_token = request.COOKIES.get('access')
        
        # 2. Если нет в cookies, проверяем в заголовке Authorization
        if not raw_token:
            header = self.get_header(request)
            if header:
                raw_token = self.get_raw_token(header)
        
        if not raw_token:
            return None

        # 3. Валидируем токен
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
