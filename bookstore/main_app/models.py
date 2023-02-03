from django.db import models
import uuid

# Create your models here.
class Suppliers(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100)

class Products(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100)
  price = models.PositiveIntegerField()
  supplier_id = models.ForeignKey(Suppliers, on_delete = models.CASCADE)
  quantity = models.PositiveIntegerField()
  
  def __str__(self):
    return self.name

class Customers(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100)
  phone = models.IntegerField()

  def __str__(self):
    return self.name

class Orders(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  customer_id = models.ForeignKey(Customers, on_delete = models.CASCADE)

class OrderDetails(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  quantity = models.PositiveIntegerField()
  order_id = models.ForeignKey(Orders, on_delete = models.CASCADE)
  product_id = models.ForeignKey(Products, on_delete = models.CASCADE)