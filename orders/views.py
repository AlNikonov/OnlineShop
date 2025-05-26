from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderProducts
from .serializer import OrderSerializer, OrderProductSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def get_orders(request):
    orders = Order.objects.all()
    return Response(OrderSerializer(orders, many=True).data)

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'GET', 'DELETE'])
def order_details(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response(OrderSerializer(order).data)
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_orders_details(request):
    order_details = OrderProducts.objects.all()
    return Response(OrderProductSerializer(order_details, many=True).data)


@api_view(['POST'])
def create_order_product(request):
    serializer = OrderProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'GET', 'DELETE'])
def order_products_details(request, order_id):
    order_details = OrderProducts.objects.filter(order_id=order_id)
    if not order_details:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(OrderProductSerializer(order_details, many=True).data)
    elif request.method == 'DELETE':
        order_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = OrderProductSerializer(order_details, data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart(request):
    print(request.user)
    print(request.user.is_authenticated)
    return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)