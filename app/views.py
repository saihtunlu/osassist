from rest_framework.permissions import IsAuthenticated

from sale.serializers import SaleSerializers
from sale.models import Sale

from order.models import Order
from order.serializers import OrderSerializers

from supplier.models import Supplier
from supplier.serializers import SupplierSerializers

from delivery.models import Delivery
from delivery.serializers import DeliverySerializers

from customer.models import Customer
from customer.serializers import CustomerSerializers

from drf_multiple_model.views import ObjectMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from django.db.models import Q


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 10000


class MainSearch(ObjectMultipleModelAPIView):
    pagination_class = LimitPagination
    permission_classes = [IsAuthenticated]
    def get_querylist(self):
            query = self.request.query_params['query']
            store = self.request.user.store
            querieslist = []
            querieslist.append({'queryset': Order.objects.filter(
                store=store, order_no__icontains=query), 'serializer_class': OrderSerializers})
            querieslist.append({'queryset': Sale.objects.filter(
                store=store, order_no__icontains=query), 'serializer_class': SaleSerializers})
            querieslist.append({'queryset': Supplier.objects.filter(
                store=store, name__icontains=query), 'serializer_class': SupplierSerializers})
            querieslist.append({'queryset': Delivery.objects.filter(
                store=store, name__icontains=query), 'serializer_class': DeliverySerializers})
            querieslist.append({'queryset': Customer.objects.filter(
                store=store, name__icontains=query), 'serializer_class': CustomerSerializers})
            return querieslist
