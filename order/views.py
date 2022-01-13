from django.shortcuts import get_object_or_404
from app.pagination import Pagination
from .models import Order
from .serializers import OrderSerializers
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class OrderView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data['data']
        store=request.user.store
        new_order = Order(store=store)
        order_serializer = OrderSerializers(new_order, data=data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = request.GET['oid']
        store=request.user.store
        order_ = generics.get_object_or_404(
            Order, id=id,store=store)
        order_serializer = OrderSerializers(order_, many=False)
        return Response(order_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        data = request.data['data']
        store=request.user.store
        old_order = get_object_or_404(
            Order, id=data['id'],store=store)

        order_serializer = OrderSerializers(old_order, data=data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        id = request.GET['oid']
        store=request.user.store
        order = get_object_or_404(
            Order, id=id,store=store)
        order.delete()
        return Response('Success', status=status.HTTP_200_OK)


class OrdersListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers
    pagination_class = Pagination

    def get_queryset(self):
        status = self.request.GET['status']
        query=self.request.GET['query']
        store =self.request.user.store
        queryset = Order.objects.filter(store=store,status__icontains=status,code__icontains=query).order_by('-created_at')
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
        return Response(data, status=status.HTTP_200_OK)

