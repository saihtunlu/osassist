from .models import Delivery
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import DeliverySerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from app.pagination import Pagination
# Create your views here.


class Deliveries(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliverySerializers
    pagination_class = Pagination

    def get_queryset(self):
        query = self.request.GET['query']
        order_by = self.request.GET['order_by']
        store = self.request.user.store

        queryset = Delivery.objects.filter(
            store=store, name__icontains=query).order_by(order_by)
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


class SearchDelivery(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
            deliveries = Delivery.objects.filter(
                store=request.user.store, name__icontains=request.GET['query']).order_by('-created_at')
            deliveries_serializer = DeliverySerializers(deliveries, many=True)
            return Response(deliveries_serializer.data, status=status.HTTP_201_CREATED)


class AllDeliveries(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
            deliveries = Delivery.objects.filter(
                store=request.user.store).order_by('-created_at')
            deliveries_serializer = DeliverySerializers(deliveries, many=True)
            return Response(deliveries_serializer.data, status=status.HTTP_201_CREATED)


class SingleDelivery(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
            data = request.data['data']
            store=request.user.store
            new_deli=Delivery(store=store)
            delivery_serializer = DeliverySerializers(new_deli,data=data)
            if delivery_serializer.is_valid():
                delivery_serializer.save()
                return Response(delivery_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(delivery_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
            data = request.data['data']
            delivery = get_object_or_404(
                Delivery, id=data['id'])
            delivery_serializer = DeliverySerializers(delivery, data=data)
            if delivery_serializer.is_valid():
                delivery_serializer.save()
                return Response(delivery_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(delivery_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = request.GET['delivery_id']
        store = request.user.store
        delivery = get_object_or_404(
            Delivery, id=id, store=store)
        delivery_serializer = DeliverySerializers(delivery, many=False)
        return Response(delivery_serializer.data, status=status.HTTP_201_CREATED)


class RemoveMultiDeliveries(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
            data = request.data['data']
            Delivery.objects.filter(pk__in=data).delete()
            return Response('Success', status=status.HTTP_201_CREATED)
