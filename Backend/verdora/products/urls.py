from django.urls import path
from . import views
from rest_framework.views import APIView
from rest_framework.response import Response

class ProductListView(APIView):
    def get(self, request):
        return Response({"message": "Product list"})

class ProductDetailView(APIView):
    def get(self, request, pk):
        return Response({"message": f"Product {pk}"})

class CategoryListView(APIView):
    def get(self, request):
        return Response({"message": "Categories"})

class ProductSearchView(APIView):
    def get(self, request):
        return Response({"message": "Search results"})

urlpatterns = [
    path('',              views.ProductListView.as_view()),        # GET (public), POST (farmer)
    path('<int:pk>/',     views.ProductDetailView.as_view()),      # GET, PUT, DELETE
    path('categories/',   views.CategoryListView.as_view()),
    path('search/',       views.ProductSearchView.as_view()),
]