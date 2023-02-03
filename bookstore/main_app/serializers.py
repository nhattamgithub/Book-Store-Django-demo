from rest_framework import serializers
from .models import Suppliers, Products, Customers, Orders, OrderDetails

class SuppliersSerializer(serializers.ModelSerializer):
  class Meta:
    model = Suppliers
    fields = ["id", "name"]

class ProductsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Products
    fields = ["id", "name", "price", "supplier_id", "quantity"]

class CustomersSerializer(serializers.ModelSerializer):
  class Meta:
    model = Customers
    fields = ["id", "name", "phone"]

class OrdersSerializer(serializers.ModelSerializer):
  class Meta:
    model = Orders
    fields = ["id", "customer_id"]

class OrderDetailsSerializer(serializers.ModelSerializer):
  class Meta:
    model = OrderDetails
    fields = ["id", "quantity", "order_id", "product_id"]
