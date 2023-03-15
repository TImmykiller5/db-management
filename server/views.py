from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import UserSerializer, InventorySerializer, ProductsTypeSerializer, ProductTypeSerializer, TransactionSerializer, StoreSerializer
from django.contrib.auth.models import User
from .models import Inventory, SalesRecord, Store, ProductType
from rest_framework import status
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import parser


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
        try:
            year = int(request.GET.dict()['year'])
            month = int(request.GET.dict()['month'])
            day = int(request.GET.dict()['day'])
            dates = []
            currentDate = datetime.today()
            yesDate = (currentDate-timedelta(days=1)).replace(minute=0, hour=0, second=0)
            preYesDate = (currentDate-timedelta(days=2)).replace(minute=0, hour=0, second=0)
            prevRecord = SalesRecord.objects.filter(transactionDate__range = [preYesDate, currentDate]).filter(transactionType = "Sale").order_by('-totalPrice')
            
            # print(prevRecord)
            serializer = TransactionSerializer(prevRecord, many=True)
            return Response(serializer.data)

        except:
            record = SalesRecord.objects.all().order_by('-transactionDate')[:20]
            serializer = TransactionSerializer(record, many=True)
            return Response(serializer.data)

class createProduct(APIView):

    def post(self, request):
        try:
            # print('hi')
            # return Response({'hi':'hello'})
            # if len(ProductType.objects.filter(name='Layers Mash')) == 0:

            data = request.data
            Product = ProductType(
                name= data['name'],
                brand= data['brand'],
                costPrice= data['costPrice'],
                sellingPrice= data['sellingPrice'],
            )

            Product.save()
            return Response({'detain':'Product Created'})
        except:
            # print('hi')
            # return Response({'hi':'hello'})

            message = {'detail':'THIS PRODUCT ALREADY EXIST'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    

class postTransaction(APIView):

    def post(self, request):
        data = request.data
        product = data['product']
        quantity = int(data['quantity'])
        store = data['store']
        date = data['date']
        transactionType = data['transactionType']

        # 2023-03-07T14:01

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
            store = stor,
            totalPrice = produc.sellingPrice*quantity,
        )

        Record.save()

        return Response({'hello':'hi'})
    
    
class getTopProducts(APIView):
    def get(self, request):
        currentDate = datetime.today()
        preYesDate = (currentDate-timedelta(days=30)).replace(minute=0, hour=0, second=0)
        prevRecord = SalesRecord.objects.filter(transactionDate__range = [preYesDate, currentDate]).filter(transactionType = "Sale").order_by('-totalPrice')
        List = []

        recordList = {}

        for items in prevRecord:
            if items.productType.name in recordList:
                recordList[items.productType.name] += items.quantity
            else:
                recordList[items.productType.name] = items.quantity
        
        # print(prevRecord)

        for items, value in recordList.items():
            list = {} 
            list['productName'] = items
            list['quantity'] = value
            List.append(list)
            # if items.productType.name in list:
            #     list[items.productType.name] += items.quantity
            # else:
            #     list[items.productType.name] = items.quantity
            

            
        return JsonResponse(List[:4],safe=False )
    

class storeData(APIView):
    def post(self, request):
        try:    
            data = request.data
            sto = Store(
                name = data['name'],
                address = data['address']
            )
            sto.save()
            serializer = StoreSerializer(sto)

            return Response(serializer.data)
        except:
            message = {'detail':'THIS STORE ALREADY EXIST'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request):
        store = Store.objects.all()
        serializers = StoreSerializer(store, many=True)
        return Response(serializers.data)
    
    def put(self, request):
        data = request.data
        try:
                
            data = request.data
            sto = Store.objects.get(id= data['storeinstance'])
            sto.name = data['name']
            sto.address = data['address']
            sto.save()
            serializer = StoreSerializer(sto)

            return Response(serializer.data)
        except:
            message = {'detail':'PLEASE CHANGE NAME OR ADDRESS'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
