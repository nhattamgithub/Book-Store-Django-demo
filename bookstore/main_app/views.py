from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import traceback

from django.db import transaction
from .models import Products, Suppliers, Customers, Orders, OrderDetails
from .serializers import ProductsSerializer, SuppliersSerializer, CustomersSerializer, OrdersSerializer, OrderDetailsSerializer
from .helper import APIs, JSONResponse

# def getAll(model, serializer_model, *args, **kwargs):
#   try:
#     objects = model.objects.all()
#     serializer = serializer_model(objects, many=True)
#     return JSONResponse({'response' : serializer.data}, status=200)
#   except Exception as ex:
#     return JSONResponse({"error" : ex}, status=400)

# def getbyId(model, serializer_model, object_id):
#   object = model.objects.filter(id = object_id)
#   if not object:
#     return Response(
#       {"res": "object does not exists"},
#       status=status.HTTP_400_BAD_REQUEST
#     )
#   serializer = serializer_model(object, many=True)
#   return Response(serializer.data, status=status.HTTP_200_OK)

# def update_object(model, serializer_model, object_id, request):
#   object = model.objects.get(id = object_id)
#   if not object:
#     return Response(
#       {"res": "object does not exists"},
#       status=status.HTTP_400_BAD_REQUEST
#     )
#   data = JSONParser().parse(request)
#   serializer = serializer_model(object, data=data)
#   if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data, status=status.HTTP_200_OK)
#   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def delete(model, object_id):
#   object = model.objects.filter(id = object_id)
#   if not object:
#     return Response(
#       {"res": "object does not exists"},
#       status=status.HTTP_400_BAD_REQUEST
#     )
#   object.delete()
#   return Response({'message': 'object was deleted successfully!'}, status=status.HTTP_200_OK)

########## Products ##########
class GetAllProductsAPIView(APIView):
  def get(self, request, *args, **kwargs):
    return APIs.getAll(Products, ProductsSerializer)

class AddProductAPIView(APIView):
  def post(self, request, *args, **kwargs):
    data = {
      'name': request.data.get('name'),
      'price': request.data.get('price'),
      'supplier_id': request.data.get('supplier_id'),
      'quantity': request.data.get('quantity')
    }
    serializer = ProductsSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductsAPIsView(APIView):
  def get(self, request, product_id, *args, **kwargs):
    return APIs.getbyId(Products, ProductsSerializer, product_id)

  def put(self, request, product_id, *args, **kwargs):
    return APIs.update_object(Products, ProductsSerializer, product_id, request)

  def delete(self, request, product_id, *args, **kwargs):
    return APIs.delete(Products, product_id)

########## Suppliers ##########
class GetAllSuppliersAPIView(APIView):
  def get(self, request, *args, **kwargs):
    return APIs.getAll(Suppliers, SuppliersSerializer)

class AddSupplierAPIView(APIView):
  def post(self, request, *args, **kwargs):
    data = {
      'name': request.data.get('name'),
    }
    serializer = SuppliersSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SuppliersAPIsView(APIView):
  def get(self, request, supplier_id, *args, **kwargs):
    return APIs.getbyId(Suppliers, SuppliersSerializer, supplier_id)

  def put(self, request, supplier_id, *args, **kwargs):
    return APIs.update_object(Suppliers, SuppliersSerializer, supplier_id, request)

  def delete(self, request, supplier_id, *args, **kwargs):
    return APIs.delete(Suppliers, supplier_id)

########## Customers ##########
class GetAllCustomersAPIView(APIView):
  def get(self, request, *args, **kwargs):
    return APIs.getAll(Customers, CustomersSerializer)

class AddCustomerAPIView(APIView):
  def post(self, request, *args, **kwargs):
    data = {
      'name': request.data.get('name'),
      'phone': request.data.get('phone'),
    }
    serializer = CustomersSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomersAPIsView(APIView):
  def get(self, request, customer_id, *args, **kwargs):
    return APIs.getbyId(Customers, CustomersSerializer, customer_id)

  def put(self, request, customer_id, *args, **kwargs):
    return APIs.update_object(Customers, CustomersSerializer, customer_id, request)

  def delete(self, request, customer_id, *args, **kwargs):
    return APIs.delete(Customers, customer_id)

########## Orders ##########
class GetAllOrdersAPIView(APIView):
  def get(self, request, *args, **kwargs):
    return APIs.getAll(Orders, OrdersSerializer)

class ClearOrdersData(APIView):
  def delete(self, request, *args, **kwargs):
    objects = Orders.objects.all()
    objects.delete()
    return JSONResponse({"success"}, status=200)

########## Order Details ##########
class GetAllOrderDetailsAPIView(APIView):
  def get(self, request, *args, **kwargs):
    return APIs.getAll(OrderDetails, OrderDetailsSerializer)

class ClearOrderDetailsData(APIView):
  def delete(self, request, *args, **kwargs):
    objects = OrderDetails.objects.all()
    objects.delete()
    return JSONResponse({"success"}, status=200)

########## Actions ##########
class BuyProductAPIView(APIView):
  def post(self, request, *args, **kwargs):
    try:
      with transaction.atomic():
        customer_id = {
          "customer_id" : request.data.get('customer_id')
        }
        order_serial = OrdersSerializer(data = customer_id)
        if order_serial.is_valid():
          order_serial.save()
          order_detail_data = {
            'quantity': request.data.get('quantity'),
            'order_id' : order_serial.data["id"],
            'product_id': request.data.get('product_id')
          }
          order_detail_serial = OrderDetailsSerializer(data = order_detail_data)
          if order_detail_serial.is_valid():
            order_detail_serial.save()
            product = Products.objects.get(id = order_detail_serial.data["product_id"])
            product.quantity -= int(order_detail_data["quantity"])
            product.save()
            return JSONResponse({'res' : "success"},status=201)
          else:
            raise Exception(order_detail_serial.errors)
        else: 
          raise Exception(order_serial.errors)
    except Exception as ex:
      return JSONResponse({'error' : str(ex)},status=500)