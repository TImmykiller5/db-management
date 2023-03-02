from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UserSerializer, InventorySerializer, ProductsTypeSerializer, ProductTypeSerializer, TransactionSerializer
from django.contrib.auth.models import User
from .models import Inventory, SalesRecord, Store, ProductType

# Create your views here.
class getProducts(APIView):
    
    def get(self, request):
        product = ProductType.objects.all()
        serializer = ProductsTypeSerializer(product, many=True)
        return Response(serializer.data)
    
class getProduct(APIView):
    
    def get(self, request, pk):
        product = ProductType.objects.get(id=pk)
        serializer = ProductTypeSerializer(product, many=False)
        return Response(serializer.data)

class getTransactions(APIView):
    
    def get(self, request):
        record = SalesRecord.objects.all().order_by('-transactionDate')[:20]
        serializer = TransactionSerializer(record, many=True)
        return Response(serializer.data)

class createProduct(APIView):

    def post(self, request):
        data = request.data
        Product = ProductType(
            name= data['name'],
            brand= data['brand'],
            costPrice= data['costPrice'],
            sellingPrice= data['sellingPrice'],
        )

        Product.save()
        return Response({'hello':'hi'})
    

class postTransaction(APIView):

    def post(self, request):
        data = request.data
        product = data['product']
        quantity = data['quantity']
        store = data['store']
        date = data['date']
        transactionType = data['transactionType']

        

        stor = Store.objects.get(name = store)
        produc = ProductType.objects.get(name = product)

        inventory = Inventory.objects.filter(store=stor).filter(productType=produc)
        if len(inventory) == 0:
            newEntry = Inventory(
                productType = produc,
                store = stor,
                quantity = quantity,
                purchaseDate = date
            )
            newEntry.save()
        else:
            entry = inventory[0]
            if transactionType == 'Stock Purchase':
                entry.quantity += int(quantity)
            else:
                entry.quantity -= int(quantity)

            entry.save()

        Record = SalesRecord(
            productType = produc,
            quantity = quantity,
            transactionType = transactionType,
            transactionDate = date,
            store = stor
        )

        Record.save()

        return Response({'hello':'hi'})