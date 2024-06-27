# from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.validators import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def landing (request):
    content = """<div style='width:100%; height:100vh; display:flex;justify-content:center;align-items:center'>
                    <h1 style='font-size: 4rem; color:blue'>Welcom to Shop-API landing page</h1>
                </div>"""
    return HttpResponse(content)

class ProductList(APIView):
  def get(self, request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

class ProductDetail(APIView):
  def get_object(self, pk):
    try:
      product = Product.objects.get(pk=pk)
      return product
    except Product.DoesNotExist:
      return None

  def get(self, request, pk):
    product = self.get_object(pk)
    if not product:
      return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

class ProductCreate(APIView):
#   permission_classes = [IsAuthenticated]
  @method_decorator(csrf_exempt)
  def post(self, request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdate(APIView):
#   permission_classes = [IsAuthenticated]

  def get_object(self, pk):
    try:
      product = Product.objects.get(pk=pk)
      return product
    except Product.DoesNotExist:
      return None

  @method_decorator(csrf_exempt)
  def put(self, request, pk):
    product = self.get_object(pk)
    if not product:
      return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class ProductDelete(APIView):
  # permission_classes = [IsAuthenticated]

  def get_object(self, pk):
    try:
      product = Product.objects.get(pk=pk)
      return product
    except Product.DoesNotExist:
      return None

  @method_decorator(csrf_exempt)
  def delete(self, request, pk):
    product = self.get_object(pk)
    if not product:
      return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if product has any associated orders before deletion (optional)
    # if Order.objects.filter(product=product).exists():
    #   return Response({'error': 'Cannot delete product with associated orders.'}, status=status.HTTP_400_BAD_REQUEST)

    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class OrderDetail(APIView):
#   permission_classes = [IsAuthenticated]

  def get_object(self, pk):
    try:
      order = Order.objects.get(pk=pk)  # Filter by user
      return order
    except Order.DoesNotExist:
      return None

  def get(self, request, pk):
    order = self.get_object(pk)
    if not order:
      return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order)
    
    return Response(serializer.data)
  

  @method_decorator(csrf_exempt)
  def put(self, request, pk):
    order = self.get_object(pk)
    if not order:
      return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if update request is for cancellation (status change)
    if 'status' in request.data and request.data['status'] == 'CANCELLED':
      if order.status == 'PENDING':  # Allow cancellation only for pending orders
        order.status = 'CANCELLED'
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
      else:
        return Response({'error': 'Order cannot be cancelled at this stage.'}, status=status.HTTP_400_BAD_REQUEST)

    # Disallow other updates through PUT (implement separate views if needed)
    return Response({'error': 'Only order cancellation (status=CANCELLED) is supported through PUT requests.'}, status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
#   permission_classes = [IsAuthenticated]

  def get(self, request):
    orders = Order.objects.filter()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
  

class OrderDelete(APIView):
  # permission_classes = [IsAuthenticated]

  def get_object(self, pk):
    try:
      order = Order.objects.get(pk=pk)  # Filter by user
      return order
    except Order.DoesNotExist:
      return None

  def delete(self, request, pk):
    order = self.get_object(pk)
    if not order:
      return Response(status=status.HTTP_404_NOT_FOUND)

    # Allow deletion only for pending orders (optional)
    if order.status != 'PENDING':
      return Response({'error': 'Cannot delete non-pending orders.'}, status=status.HTTP_400_BAD_REQUEST)

    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  


class OrderCreate(APIView):
  # permission_classes = [IsAuthenticated]

  def post(self, request):
      # serializer = OrderSerializer(instance=order, depth = 2)  
      serializer = OrderSerializer(data=request.data)
      if serializer.is_valid():
          # Get product from request data
          product_id = request.data.get('product')
          if not product_id:
              raise ValidationError({'product': 'Missing product ID in request data.'})

          try:
              product = Product.objects.get(pk=product_id)
          except Product.DoesNotExist:
              raise ValidationError({'product': 'Invalid product ID provided.'})

          # Check product availability
          if product.available_quantity < 1:
              raise ValidationError({'product': 'Insufficient product quantity.'})

          # Reduce product quantity by ordered amount
          requested_product_quantity = request.data.get('quantity')
          product.available_quantity -= int(requested_product_quantity)
          product.save()

          serializer.save()  # Save the order instance
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

