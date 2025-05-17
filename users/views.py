from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import RegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

@api_view(['POST'])
def create_user(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'login': user.login
        })
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    login = request.data.get('login', None)
    password = request.data.get('password', None)
    if login is None or password is None:
        return Response({'error': 'Login and password required'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(login=login, password=password)
    if user is None:
        return Response({'error': 'No such user'},

                        status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    refresh.payload.update({
        'user_id': user.id,
        'login': user.login
    })
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def logout(request):
    refresh = request.data.get('refresh_token')
    if not refresh:
        return Response({ 'error': 'Refresh Token Required' }, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh)
        token.blacklist()
    except Exception as e:
        return Response({'error': 'Invalid Refresh Token'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'success': 'Logout successfull'}, status=status.HTTP_200_OK)