from .models import Customer, CustomerAddress
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import CustomerSerializers, CustomerAddressSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from app.pagination import Pagination
from django.db.models import Q

# Create your views here.


class Customers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializers
    pagination_class = Pagination

    def get_queryset(self):
        store = self.request.user.store
        query = self.request.GET['query']
        order_by = self.request.GET['order_by']

        queryset = Customer.objects.filter(
            Q(store=store, name__icontains=query) | Q(store=store, email__icontains=query) | Q(store=store, phone__icontains=query)).order_by(order_by)
        return queryset

    def get(self, request):
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                result = self.get_paginated_response(serializer.data)
                data = result.data  # pagination data
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)


class SearchCustomer(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
            customers = Customer.objects.filter(
                store=request.user.store, name__icontains=request.GET['query']).order_by('-created_at')
            customer_serializer = CustomerSerializers(customers, many=True)
            return Response(customer_serializer.data, status=status.HTTP_201_CREATED)


class SingleCustomer(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
            data = request.data['data']
            customer = Customer()
            customer_serializer = CustomerSerializers(customer, data=data)
            if customer_serializer.is_valid():
                customer_serializer.save()
                new_address = CustomerAddress(customer=customer)
                address_serializer = CustomerAddressSerializers(
                    new_address, data=data['address'])
                if address_serializer.is_valid():
                    address_serializer.save()
                return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
            data = request.data['data']
            id = request.GET['cid']
            customer = get_object_or_404(
                Customer, id=id)
            customer_serializer = CustomerSerializers(customer, data=data)
            if customer_serializer.is_valid():
                customer_serializer.save()
                address = CustomerAddress.objects.get_or_create(
                    customer=customer)[0]
                address_serializer = CustomerAddressSerializers(
                    address, data=data['address'])
                if address_serializer.is_valid():
                    address_serializer.save()
                return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = request.GET['cid']
        store = request.user.store
        customer = get_object_or_404(
            Customer, id=id, store=store)
        customer_serializer = CustomerSerializers(customer, many=False)
        return Response(customer_serializer.data, status=status.HTTP_201_CREATED)


class RemoveMultiCustomers(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
            data = request.data['data']
            Customer.objects.filter(pk__in=data).delete()
            return Response('Success', status=status.HTTP_201_CREATED)
