from rest_framework import serializers
from .models import Product, Order
# from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ['id', 'title', 'description', 'price', 'available_quantity']




class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Assuming you need product details
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
#    user = UserSerializer(read_only=True)  # Uncomment if you need user details

    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'created_at', 'status']
        depth = 1


