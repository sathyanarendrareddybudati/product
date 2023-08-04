from django.urls import path
from .views import FetchproductsdataAPI, ProductfiltersAPI, ProductlistAPI

urlpatterns = [
    path('fetch_products/', FetchproductsdataAPI.as_view(), name='fetch_products'),
    path('product_filters/', ProductfiltersAPI.as_view(), name='product_filters'),
    path('product_list/', ProductlistAPI.as_view(), name='product_list'),
]
