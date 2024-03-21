from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer
from .serializers import CustomerSerializer, CustomerListSerializer


class CustomerListView(APIView):
    @staticmethod
    def get(request):
        customers = Customer.objects.filter(is_active=True)
        serializer = CustomerListSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerCreateView(APIView):
    @staticmethod
    def post(request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Customer.objects.get(pk=pk)
        except:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        customer.is_active = False
        customer.save()
        return JsonResponse({"message": "Customer deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
