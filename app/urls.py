from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createproduct', views.create_product, name='create_product'),
    path('transactiondetail/<int:pk>', views.transaction_detail, name='transactiondetail'),
    path('productdetail/<int:pk>', views.product_detail, name='productdetail'),
]
