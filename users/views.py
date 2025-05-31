from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import RegistrationSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, update_session_auth_hash

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')
        
        if not refresh_token:
            return Response(
                {'detail': 'Refresh token not found in cookies'},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)
        response.set_cookie('access', response.data.get('access'), httponly=True)
        return response

@api_view(['POST'])
def create_user(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })
        response = Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)
        response.set_cookie('refresh', refresh, httponly=True)
        response.set_cookie('access', refresh.access_token, httponly=True)
        return response
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    if username is None or password is None:
        return Response({'error': 'Login and password required'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'No such user'},

                        status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    refresh.payload.update({
        'user_id': user.id,
        'username': user.username
    })
    response = Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)
    response.set_cookie('refresh', refresh, httponly=True)
    response.set_cookie('access', refresh.access_token, httponly=True)
    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh = request.COOKIES.get('refresh')
    if not refresh:
        return Response({ 'error': 'Refresh Token Required' }, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh)
        print(type(token))
        token.blacklist()

    except Exception as e:
        print(e)
        return Response({'error': 'Invalid Refresh Token'}, status=status.HTTP_400_BAD_REQUEST)
    response = Response({'success': 'Logout successfull'}, status=status.HTTP_200_OK)
    response.delete_cookie('refresh')
    response.delete_cookie('access')
    return response

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    users = User.objects.all()
    print(users)

    return Response(UserSerializer(users, many=True).data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    token = RefreshToken(request.COOKIES.get('refresh'))
    user = User.objects.get(id=token['user_id'])
    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    oldpwd = request.data['oldpwd']
    newpwd = request.data['newpwd']
    if not request.user.check_password(oldpwd):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    request.user.set_password(newpwd)
    request.user.save()
    return Response(status=status.HTTP_200_OK)