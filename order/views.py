from django.shortcuts import get_object_or_404
from supplier.models import Supplier
from app.pagination import Pagination
from .models import Order, OrderProduct
from .serializers import OrderProductSerializers, OrderSerializers
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.template.loader import render_to_string
from django.http import HttpResponse


def print_order(order):
    template_path = 'pdf/order/default.html'
    html = render_to_string(
        template_path, {'order': order})
    response = HttpResponse(html, content_type='application/html')
    filename = 'order.html'
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        filename)
    return response


class OrderView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data['data']
        store=request.user.store
        new_order = Order(store=store)
        if 'supplier_name' in data and data['supplier_name'] != '':
            supplier= Supplier.objects.get_or_create(
                name=data['supplier_name'],store=store)[0]
            new_order.supplier = supplier
        order_serializer = OrderSerializers(new_order, data=data)
        if order_serializer.is_valid():
            order_serializer.save()
            if 'products' in data:
                for order_product in data['products']:
                    order_product_model = OrderProduct(order=new_order)
                    order_product_serializer = OrderProductSerializers(
                        order_product_model, data=order_product)
                    if order_product_serializer.is_valid():
                        order_product_serializer.save()
                    else:
                        new_order.delete()
                        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
      
        if 'supplier_name' in data and data['supplier_name'] != '':
            delivery= Supplier.objects.get_or_create(
                name=data['supplier_name'],store=store)[0]
            old_order.supplier = delivery

        order_serializer = OrderSerializers(old_order, data=data)
        if order_serializer.is_valid():
            order_serializer.save()
            for order_product in data['products']:
                    if 'id' in order_product:
                        order_product_model = get_object_or_404(
                            OrderProduct, id=order_product['id'])
                    else:
                        order_product_model = OrderProduct.objects.create(
                            name=order_product['name'], order=old_order
                        )
                    order_product_serializer = OrderProductSerializers(
                        order_product_model, data=order_product)
                   
                    if order_product_serializer.is_valid():
                        order_product_serializer.save()
                    else:
                        return Response(order_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers
    pagination_class = Pagination

    def get_queryset(self):
        date = self.request.GET['date']
        supplier = self.request.GET['supplier']
        order_by = self.request.GET['order_by']
        query=self.request.GET['query']
        store =self.request.user.store
        queryset = Order.objects.filter(
            supplier__name__icontains=supplier,store=store,date__icontains=date,note__icontains=query).order_by(order_by)
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



class OrdersView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        oid = request.GET['oid']
        sid = request.GET['sid']
        date = request.GET['date']
        order_ = generics.get_object_or_404(
            Order, id=oid,store__pk=sid,date=date)
        order_serializer = OrderSerializers(order_, many=False)
        return Response(order_serializer.data, status=status.HTTP_200_OK)
