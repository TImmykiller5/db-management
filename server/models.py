from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class ProductType(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    brand = models.CharField(max_length=200, null=True, blank=True)
    costPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    sellingPrice = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return self.name

class Inventory(models.Model):
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    purchaseDate = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.productType.name

   

class SalesRecord(models.Model):
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True)
    quantity =  models.IntegerField(null=True, blank=True, default=0)
    transactionType = models.CharField(max_length=200, null=True, blank=True)
    transactionDate = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    totalPrice = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.productType.name