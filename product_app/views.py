import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Product, Comment
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from urllib.parse import urlencode
import math


class FetchproductsdataAPI(APIView):

    def get(self, request):

        product_api_url = "https://dummyjson.com/products?limit=200"
        response = requests.get(product_api_url)
        if response.status_code == 200:
            products_data = response.json()['products']
            for product_data in products_data:
            
                selected_fields = {
                    'title': product_data['title'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'discount_percentage': product_data['discountPercentage'],
                    'rating': product_data['rating'],
                    'stock': product_data['stock'],
                    'brand': product_data['brand'],
                    'category': product_data['category'],
                    'thumbnail': product_data['thumbnail'],
                    'images': product_data['images'],
                }
                product = Product.objects.create(**selected_fields)

                product_comments_api_url = f"https://dummyjson.com/posts/{product_data['id']}/comments"
                comments_response = requests.get(product_comments_api_url)
                if comments_response.status_code == 200:
                    comments_data = comments_response.json()['comments']
            
                    for comment_data in comments_data:
                        comment = Comment.objects.create(
                            body=comment_data['body'],
                            post_id=comment_data['postId'],
                            user_id=comment_data['user']['id'],
                            username=comment_data['user']['username'],
                            product=product
                        )
            return Response({"message": "Products data fetched and saved successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to fetch products data."}, status=response.status_code)


class ProductfiltersAPI(APIView):

    def get(self, request):
        
        filters_data = request.data 
        filter_params = {}

        for key, value in filters_data.items():
            if isinstance(value, list):  
                filter_params[key] = ",".join(value)
            else:
                filter_params[key] = value

        product_list_url = f"{request.build_absolute_uri('/product_list/')}?{urlencode(filter_params)}"

        return Response({"product_list_url": product_list_url}, status=status.HTTP_200_OK)

        
class ProductlistAPI(APIView):

    def get(self, request):
        
        queryset = Product.objects.all()
        filters = {}

        for key, value in request.query_params.items():
            if key not in ['page', 'page_size']:
                if ',' in value:
                    values = value.split(',')
                    filters[key + '__in'] = values
                else:
                    filters[key] = value
                    
        if filters:
            queryset = queryset.filter(**filters)
        
        paginator = PageNumberPagination()
        paginator.page_size = int(request.query_params.get('page_size', 10))
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(result_page, many=True)

        data = {
            "count": paginator.page.paginator.count,
            "current_page": paginator.page.number,
            "total_pages": math.ceil(paginator.page.paginator.count/paginator.page_size),
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

