from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Inventory, ProductType, Store, SalesRecord
import decimal

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']


class InventorySerializer (serializers.ModelSerializer):
    store = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'
    
    def get_store(self, obj):
        store = obj.store
        serializers = StoreSerializer(store, many=False)
        return serializers.data

class ProductsTypeSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductType
        fields = '__all__'

    def get_quantity(self, obj):
        products = obj.inventory_set.all()
        
        quantity = 0
        for product in products:
            quantity += product.quantity
        return quantity
    
    


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    ProductName = serializers.SerializerMethodField(read_only=True)
    ProductPrice = serializers.SerializerMethodField(read_only=True)
    

    class Meta:
        model = SalesRecord
        fields = '__all__'
    
    def get_ProductName(self, obj):
            products = obj.productType
            serializers = ProductsTypeSerializer(products, many=False)
            return serializers.data['name']
    
    def get_ProductPrice(self, obj):
            products = obj.productType
            serializers = ProductsTypeSerializer(products, many=False)
            return serializers.data['sellingPrice']
    
    # def get_TotalPrice(self, obj):
    #         products = obj.productType
    #         serializers = ProductsTypeSerializer(products, many=False)
    #         return (float(serializers.data['sellingPrice']) * (obj.quantity))


class ProductTypeSerializer(serializers.ModelSerializer):
    inventory = serializers.SerializerMethodField(read_only=True)
    quantity = serializers.SerializerMethodField(read_only=True)
    store = serializers.SerializerMethodField(read_only=True)

    

    class Meta:
        model = ProductType
        fields = '__all__'

    
    def get_inventory(self, obj):
        products = obj.inventory_set.all()
        serializers = InventorySerializer(products, many=True)
        return serializers.data

    def get_quantity(self, obj):
        products = obj.inventory_set.all()
        quantity = 0
        for product in products:
            quantity += product.quantity
        return quantity
    
    def get_store(self, obj):
        store = Store.objects.all()
        serializers = StoreSerializer(store, many=True)
        return serializers.data
    

# class MonthlyReview(serializers.ModelSerializer):
#     model = SalesRecord

    
class StoreInventorySerializer (serializers.ModelSerializer):
    productName = serializers.SerializerMethodField(read_only=True)
    costPrice = serializers.SerializerMethodField(read_only=True)
    sellingPrice = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'

    def getProduct(self, obj):
        product = obj.productType

        serializers = ProductTypeSerializer(product, many=False)
        return serializers.data
        
    

    def get_productName(self, obj):
        global m
        m = self.getProduct(obj)
        return self.getProduct(obj)['name']
    
    def get_costPrice(self, obj):
        
        return m['costPrice']
    
    def get_sellingPrice(self, obj):
        return m['sellingPrice']