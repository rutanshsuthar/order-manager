# products/views.py
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.utils import standard_response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class ProductListCreateView(APIView):
    def get(self, request, format=None):
        try:
            products = Product.objects.filter(is_active=True)
            serializer = ProductSerializer(products, many=True)
            return standard_response(True, "Products retrieved successfully", serializer.data)
        except Exception as e:
            return standard_response(False, "Failed to retrieve products", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return standard_response(True, "Product created successfully", serializer.data,
                                         status_code=status.HTTP_201_CREATED)
            return standard_response(False, "Validation failed", error=serializer.errors,
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return standard_response(False, "Validation error", error=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return standard_response(False, "Failed to create product", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk, is_active=True)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found.", code=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        try:
            product = self.get_object(pk)
            serializer = ProductSerializer(product)
            return standard_response(True, "Product retrieved successfully", serializer.data)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return standard_response(False, "Failed to retrieve product", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            product = self.get_object(pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return standard_response(True, "Product updated successfully", serializer.data)
            return standard_response(False, "Validation failed", error=serializer.errors,
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return standard_response(False, "Validation error", error=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return standard_response(False, "Failed to update product", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        try:
            product = self.get_object(pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return standard_response(False, "Failed to delete product", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryListCreateView(APIView):
    def get(self, request, format=None):
        try:
            categories = Category.objects.filter(parent__isnull=True, is_active=True)
            serializer = CategorySerializer(categories, many=True)
            return standard_response(True, "Categories retrieved successfully", serializer.data)
        except Exception as e:
            return standard_response(False, "Failed to retrieve categories", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return standard_response(True, "Category created successfully", serializer.data,
                                         status_code=status.HTTP_201_CREATED)
            return standard_response(False, "Validation failed", error=serializer.errors,
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return standard_response(False, "Validation error", error=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return standard_response(False, "Failed to create category", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk, is_active=True)
        except Category.DoesNotExist:
            raise NotFound(detail="Category not found.", code=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        try:
            category = self.get_object(pk)
            serializer = CategorySerializer(category)
            return standard_response(True, "Category retrieved successfully", serializer.data)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return standard_response(False, "Failed to retrieve category", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            category = self.get_object(pk)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return standard_response(True, "Category updated successfully", serializer.data)
            return standard_response(False, "Validation failed", error=serializer.errors,
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return standard_response(False, "Validation error", error=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return standard_response(False, "Failed to update category", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        try:
            category = self.get_object(pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return standard_response(False, "Failed to delete category", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
