from .models import Supplier, BankAccountInformation
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from app.pagination import Pagination
from rest_framework.response import Response
from .serializers import SupplierSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
# Create your views here.


class SearchSupplier(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
            suppliers = Supplier.objects.filter(
                store=request.user.store, name__icontains=request.GET['query']).order_by('-created_at')
            supplier_serializer = SupplierSerializers(suppliers, many=True)
            return Response(supplier_serializer.data, status=status.HTTP_201_CREATED)


class Suppliers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierSerializers
    pagination_class = Pagination

    def get_queryset(self):
        query = self.request.GET['query']
        order_by = self.request.GET['order_by']
        store = self.request.user.store
        queryset = Supplier.objects.filter(
            name__icontains=query, store=store).order_by(order_by)
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


class SingleSupplier(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        data = request.data['data']
        supplier_serializer = SupplierSerializers(data=data)
        if supplier_serializer.is_valid():
            supplier_serializer.save()
            return Response(supplier_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(supplier_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data['data']
        supplier = get_object_or_404(
            Supplier, id=data['id'])
        supplier_serializer = SupplierSerializers(supplier, data=data)
        if supplier_serializer.is_valid():
            supplier_serializer.save()
            return Response(supplier_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(supplier_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = request.GET['supplier_id']
        store = request.user.store
        supplier = get_object_or_404(
            Supplier, id=id, store=store)
        supplier_serializer = SupplierSerializers(supplier, many=False)
        return Response(supplier_serializer.data, status=status.HTTP_201_CREATED)


class RemoveMultiSuppliers(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data['data']
        Supplier.objects.filter(pk__in=data).delete()
        return Response('Success', status=status.HTTP_201_CREATED)
