# orders/views.py
import requests
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView

from utils.utils import standard_response
from .models import Order
from .serializers import OrderSerializer


class OrderListCreateView(APIView):
    def get(self, request, format=None):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return standard_response(True, "Orders retrieved successfully", serializer.data)
        except Exception as e:
            return standard_response(False, "Failed to retrieve orders", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        try:
            if serializer.is_valid():
                order = serializer.save()
                pdf_generation_url = request.build_absolute_uri('/presigned-urls/generate-upload-pdf/')
                payload = {'order_id': order.id}
                headers = {'Content-Type': 'application/json'}
                requests.post(pdf_generation_url, json=payload, headers=headers)
                return standard_response(True, "Order created successfully", serializer.data,
                                         status_code=status.HTTP_201_CREATED)
            return standard_response(False, "Validation failed", error=serializer.errors,
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return standard_response(False, "Validation error", error=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return standard_response(False, "Failed to create order", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise NotFound(detail="Order not found.", code=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        try:
            order = self.get_object(pk)
            serializer = OrderSerializer(order)
            return standard_response(True, "Order retrieved successfully", serializer.data)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return standard_response(False, "Failed to retrieve order", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            order = self.get_object(pk)
            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return standard_response(True, "Order updated successfully", serializer.data)
            return standard_response(False, "Validation failed", error=serializer.errors,
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return standard_response(False, "Validation error", error=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return standard_response(False, "Failed to update order", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        try:
            order = self.get_object(pk)
            order.delete()
            return standard_response(True, "Order deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return standard_response(False, "Failed to delete order", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
