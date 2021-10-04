from customer.models import Customer,CustomerAddress
from customer.serializers import CustomerAddressSerializers
from .models import Sale, SaleAddress, SaleProduct, SalePayment
from .serializers import SaleAddressSerializers, SaleProductSerializers, SaleSerializers, SaleListSerializers, SalePaymentSerializers
from rest_framework import status
from rest_framework import generics
from app.pagination import Pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncDate
from django.db.models import Count, Sum
from django.db.models import Q
from delivery.models import Delivery
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string

class Sales(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SaleListSerializers
    pagination_class = Pagination

    def get_queryset(self):
        query = self.request.GET['query']
        status = self.request.GET['status']
        date = self.request.GET['date']
        delivery = self.request.GET['delivery']
        order_by = self.request.GET['order_by']
        store=self.request.user.store
        if status == 'Unfulfilled':
            status = False
            queryset = Sale.objects.filter(
                Q(store=store,sale_no__icontains=query, is_fulfilled=status,  date__icontains=date, delivery_company__name__icontains=delivery) |
                Q(store=store,sale_no__icontains=query, is_fulfilled=status, date__icontains=date,  delivery_company__isnull=True) |
                Q(store=store,customer__name__icontains=query, is_fulfilled=status, date__icontains=date,  delivery_company__name__icontains=delivery) |
                Q(store=store,customer__name__icontains=query, is_fulfilled=status,
                  date__icontains=date,  delivery_company__isnull=True)
            ).order_by(order_by)
        else:
            queryset = Sale.objects.filter(
                Q(store=store,sale_no__icontains=query, status__icontains=status,  date__icontains=date, delivery_company__name__icontains=delivery) |
                Q(store=store,sale_no__icontains=query, status__icontains=status, date__icontains=date,  delivery_company__isnull=True) |
                Q(store=store,customer__name__icontains=query, status__icontains=status, date__icontains=date,  delivery_company__name__icontains=delivery) |
                Q(store=store,customer__name__icontains=query, status__icontains=status, date__icontains=date,  delivery_company__isnull=True) |

                Q(store=store,sale_no__icontains=query, payment_status=status,  date__icontains=date, delivery_company__name__icontains=delivery) |
                Q(store=store,sale_no__icontains=query, payment_status=status, date__icontains=date,  delivery_company__isnull=True) |
                Q(store=store,customer__name__icontains=query, payment_status=status, date__icontains=date,  delivery_company__name__icontains=delivery) |
                Q(store=store,customer__name__icontains=query, payment_status=status,
                  date__icontains=date,  delivery_company__isnull=True)

            ).order_by(order_by)
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


class SaleProducts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SaleProductSerializers
    pagination_class = Pagination

    def get_queryset(self):
        query = self.request.GET['query']
        store=self.request.user.store
        date = self.request.GET['date']
        queryset = SaleProduct.objects.filter(
           store=store, name__icontains=query, date__icontains=date).order_by('-updated_at')
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


class SingleSale(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data['data']
        store=request.user.store
        new_sale = Sale(store=store)
        
        if 'customer_name' in data and data['customer_name'] != '':
            customer,is_new_customer= Customer.objects.get_or_create(
                name=data['customer_name'],store=store)
            if is_new_customer:
                customer.phone=data['phone']
                if data['address']:
                    customer_address_model = CustomerAddress(customer=customer)
                    customer_address_serializer = CustomerAddressSerializers(
                        customer_address_model, data=data['address'])
                    if customer_address_serializer.is_valid():
                        customer_address_serializer.save()
                customer.save()
            new_sale.customer = customer

        if 'delivery_company_name' in data and data['delivery_company_name'] != '':
            delivery= Delivery.objects.get_or_create(
                name=data['delivery_company_name'],store=store)[0]
            new_sale.delivery_company = delivery

        sale_serializer = SaleSerializers(new_sale, data=data)
        if sale_serializer.is_valid():
            sale_serializer.save()
            if data['products']:
                for sale_product in data['products']:
                    sale_product_model = SaleProduct(sale=new_sale,store=store)
                    sale_product_serializer = SaleProductSerializers(
                        sale_product_model, data=sale_product)
                    if sale_product_serializer.is_valid():
                        sale_product_serializer.save()
                    else:
                        new_sale.delete()
                        return Response(sale_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if data['address']:
                    sale_address_model = SaleAddress(sale=new_sale)
                    sale_address_serializer = SaleAddressSerializers(
                        sale_address_model, data=data['address'])
                    if sale_address_serializer.is_valid():
                        sale_address_serializer.save()
                    else:
                        new_sale.delete()
                        return Response(sale_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            new_sale.sale_no = '#'+str(new_sale.id).zfill(4)
            new_sale.save()
            return Response(sale_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data['data']
        store=request.user.store
        old_sale = get_object_or_404(
            Sale, id=data['id'],store=store)
      
        if 'customer_name' in data and data['customer_name'] != '':
            customer,is_new_customer = Customer.objects.get_or_create(
                name=data['customer_name'],store=store)
            if is_new_customer:
                customer.phone=data['phone']
                if data['address']:
                    customer_address_model = CustomerAddress(customer=customer)
                    customer_address_serializer = CustomerAddressSerializers(
                        customer_address_model, data=data['address'])
                    if customer_address_serializer.is_valid():
                        customer_address_serializer.save()
                customer.save()
            old_sale.customer = customer
        if 'delivery_company_name' in data and data['delivery_company_name'] != '':
            delivery= Delivery.objects.get_or_create(
                name=data['delivery_company_name'],store=store)[0]
            old_sale.delivery_company = delivery
          

        sale_serializer = SaleSerializers(old_sale, data=data)
        if sale_serializer.is_valid():
            sale_serializer.save()
            if data['products']:
                for sale_product in data['products']:
                    if 'id' in sale_product:
                        sale_product_model = get_object_or_404(
                            SaleProduct, id=sale_product['id'])
                    else:
                        sale_product_model = SaleProduct.objects.create(
                            name=sale_product['name'], sale=old_sale,store=store
                        )
                    sale_product_serializer = SaleProductSerializers(
                        sale_product_model, data=sale_product)
                   
                    if sale_product_serializer.is_valid():
                        sale_product_serializer.save()
                       
                    else:
                        return Response(sale_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if data['address']:
                    sale_address_model = SaleAddress.objects.get_or_create(
                sale=old_sale)[0]
                    sale_address_serializer = SaleAddressSerializers(
                        sale_address_model, data=data['address'])
                    
                    if sale_address_serializer.is_valid():
                        sale_address_serializer.save()
                    else:
                        return Response(sale_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(sale_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = request.GET['sid']
        store=request.user.store
        sale = get_object_or_404(
            Sale, id=id,store=store)
        sale_serializer = SaleSerializers(sale, many=False)
        return Response(sale_serializer.data, status=status.HTTP_200_OK)


class SingleSaleProduct(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        id = request.GET['spid']
        store=request.user.store
        sale_product = get_object_or_404(
            SaleProduct, id=id,store=store)
        sale_product.delete()
        return Response('Success', status=status.HTTP_200_OK)


class SingleOrderPayment(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data['data']
        store=request.user.store
        payment_status = data['payment_status']
        sale = Sale.objects.get(id=data['sale_id'],store=store)
        sale.due_amount = int(sale.total) - int(data['amount'])
        sale.payment_status = payment_status
        sale.save()
        salePayment = SalePayment(sale=sale,store=store)
        payment_serializer = SalePaymentSerializers(
            salePayment, data=data)
        if payment_serializer.is_valid():
            payment_serializer.save()
            return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaleReport(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        store=request.user.store
        today_date = request.GET['today']
        from_date = request.GET['from']
        to_date = request.GET['to']

        today_sale_number = list(Sale.objects.filter(created_at__icontains=today_date,store=store).annotate(dates=TruncDate(
            'created_at')).values('dates').annotate(count=Count('id')).values('dates', 'count').order_by('dates'))
        today_sale_prices = list(SaleProduct.objects.filter(store=store,created_at__icontains=today_date).annotate(dates=TruncDate(
            'created_at')).values('dates').annotate(price=Sum('subtotal')).values('dates', 'price').order_by('dates'))
        today_received_amounts = list(SalePayment.objects.filter(store=store,created_at__icontains=today_date).annotate(dates=TruncDate(
            'created_at')).values('dates').annotate(price=Sum('amount')).values('dates', 'price').order_by('dates'))

        sale_number = list(Sale.objects.filter(store=store,created_at__range=([from_date, to_date])).annotate(dates=TruncDate(
            'created_at')).values('dates').annotate(count=Count('id')).values('dates', 'count').order_by('dates'))
        sale_prices = list(SaleProduct.objects.filter(store=store,created_at__range=([from_date, to_date])).annotate(dates=TruncDate(
            'created_at')).values('dates').annotate(price=Sum('subtotal')).values('dates', 'price').order_by('dates'))
        received_amounts = list(SalePayment.objects.filter(store=store,created_at__range=([from_date, to_date])).annotate(dates=TruncDate(
            'created_at')).values('dates').annotate(price=Sum('amount')).values('dates', 'price').order_by('dates'))

        data = {
            'sale_numbers': {
                'label': [],
                'data': [],
            },
            'sale_prices': {
                'label': [],
                'data': [],
            },
            'received_amount': {
                'label': [],
                'data': [],
            },
            'today_data': {
                'sale_prices': '',
                'received_amounts': '',
                'sale_numbers': ''
            }
        }
        try:
            data['today_data']['sale_prices'] = today_sale_prices[0]['price']
        except:
            pass
        try:
            data['today_data']['received_amounts'] = today_received_amounts[0]['price']
        except:
            pass
        try:
            data['today_data']['sale_numbers'] = today_sale_number[0]['count']
        except:
            pass

        for received_amount in received_amounts:
            data['received_amount']['data'].append(
                received_amount['price'])
            data['received_amount']['label'].append(
                received_amount['dates'])

        for prices in sale_prices:
            data['sale_prices']['label'].append(prices['dates'])
            data['sale_prices']['data'].append(prices['price'])

        for prices in sale_number:
            data['sale_numbers']['label'].append(prices['dates'])
            data['sale_numbers']['data'].append(prices['count'])

        return Response(data, status=status.HTTP_200_OK)


class Fulfill(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
            data = request.data['data']
            sale = get_object_or_404(
                Sale, id=request.data['sale_id'])
            sale.is_fulfilled=request.data['is_fulfilled']
            for product in data:
                sale_product = SaleProduct.objects.get(id=product['id'])
                sale_product.number_of_fullfilled = product['number_of_fullfilled']
                sale_product.save()
            return Response('Success', status=status.HTTP_201_CREATED)

class Invoices(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
            data = request.data['data']
            store = request.user.store
            sale = get_object_or_404(
                Sale, id=data['sale_id'], store=store)
            sale_serializer = SaleSerializers(sale, many=False)
            template_path = 'pdf/sale/invoice.html'
            html = render_to_string(
                template_path, {'sale': sale_serializer.data, "store":store})
            return Response(html, status=status.HTTP_200_OK)

class SalesStatus(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
            status_ = request.data['status']
            ids = request.data['ids']
            sales = Sale.objects.filter(pk__in=ids)
            for sale in sales:
                sale.status = status_
                sale.save()
            return Response('Success', status=status.HTTP_201_CREATED)


class GetOrderProducts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
            deliveries = SaleProduct.objects.filter(
                store=request.user.store, sale__date__icontains=request.GET['date']).order_by('-created_at')
            deliveries_serializer = SaleProductSerializers(deliveries, many=True)
            return Response(deliveries_serializer.data, status=status.HTTP_201_CREATED)
