# customers/views.py
from rest_framework import filters, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.utils import standard_response
from .models import Customer
from .serializers import CustomerSerializer


class CustomerListCreateView(APIView):
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', '^phone_number']

    def get(self, request, format=None):
        try:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
            return standard_response(True, "Customers retrieved successfully", serializer.data)
        except Exception as e:
            return standard_response(False, "Failed to retrieve customers", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return standard_response(True, "Customer created successfully", serializer.data,
                                         status_code=status.HTTP_201_CREATED)
            return standard_response(False, "Validation failed", error=serializer.errors,
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return standard_response(False, "Validation error", error=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return standard_response(False, "Failed to create customer", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk, is_active=True)
        except Customer.DoesNotExist:
            raise NotFound(detail="Customer not found.", code=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        try:
            customer = self.get_object(pk)
            serializer = CustomerSerializer(customer)
            return standard_response(True, "Customer retrieved successfully", serializer.data)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return standard_response(False, "Failed to retrieve customer", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            customer = self.get_object(pk)
            serializer = CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return standard_response(True, "Customer updated successfully", serializer.data)
            return standard_response(False, "Validation failed", error=serializer.errors,
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return standard_response(False, "Validation error", error=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return standard_response(False, "Failed to update customer", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        try:
            customer = self.get_object(pk)
            customer.is_active = False
            customer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return standard_response(False, str(e), status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return standard_response(False, "Failed to delete customer", error=str(e),
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
