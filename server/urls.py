from django.urls import path
from . import views

urlpatterns = [
    path('products/',  views.getProducts.as_view(), name='products'),
    path('store/<str:pk>/',  views.getStore.as_view(), name='store'),
    path('add-product/',  views.createProduct.as_view(), name='createProduct'),
    path('get-product/<str:pk>/',  views.getProduct.as_view(), name='getProduct'),
    path('get-top-product/',  views.getTopProducts.as_view(), name='getTopProduct'),
    path('get-records/',  views.getTransactions.as_view(), name='getRecords'),
    path('post-transaction/',  views.postTransaction.as_view(), name='postTransaction'),
    path('store/',  views.storeData.as_view(), name='store'),
]

