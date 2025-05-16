from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import RegistrationSerializer

@api_view(['POST'])
def create_user(request):
    user = request.data.get('user', {})
    serializer = RegistrationSerializer(data=user)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)