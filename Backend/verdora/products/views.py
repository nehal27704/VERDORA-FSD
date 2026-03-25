from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

class ProductListView(APIView):
    def get(self, request):
        return Response({"message": "Product list"})

    def post(self, request):
        return Response({"message": "Product created"})


class ProductDetailView(APIView):
    def get(self, request, pk):
        return Response({"message": f"Product {pk}"})

    def put(self, request, pk):
        return Response({"message": f"Product {pk} updated"})

    def delete(self, request, pk):
        return Response({"message": f"Product {pk} deleted"})


class CategoryListView(APIView):
    def get(self, request):
        return Response({"message": "Category list"})


class ProductSearchView(APIView):
    def get(self, request):
        return Response({"message": "Search results"})