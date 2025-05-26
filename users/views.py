from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import RegistrationSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

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
def get_users(request):
    users = User.objects.all()
    print(users)
    return Response(UserSerializer(users, many=True).data)

@api_view(['PUT', 'GET', 'DELETE'])
def user_details(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(UserSerializer(user).data)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)