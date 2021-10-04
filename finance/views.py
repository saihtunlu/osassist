from django.db.models.aggregates import Count
from .models import Finance,FinanceLabel
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import FinanceLabelSerializers, FinanceSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from app.pagination import Pagination
from django.db.models import  Sum
from django.db.models.functions import TruncDate
# Create your views here.


class Finances(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FinanceSerializers
    pagination_class = Pagination

    def get_queryset(self):
        query = self.request.GET['query']
        type = self.request.GET['type']
        date = self.request.GET['date']
        label = self.request.GET['label']
        order_by = self.request.GET['order_by']
        store = self.request.user.store

        queryset = Finance.objects.filter(
            store=store, note__icontains=query,type__icontains=type,label__name__icontains=label,date__icontains=date).order_by(order_by)
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


class SingleFinance(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
            data = request.data['data']
            store=request.user.store
            new_finance=Finance(store=store)
            if 'label_name' in data and data['label_name'] != '':
                label= FinanceLabel.objects.get_or_create(
                    name=data['label_name'],store=store)[0]
                new_finance.label = label
            finance_serializer = FinanceSerializers(new_finance,data=data)
            if finance_serializer.is_valid():
                finance_serializer.save()
                if data['type'] == 'Expense':
                    store.balance = int(store.balance) - int(data['amount'])
                elif data['type'] == 'Incomes':
                    store.balance = int(store.balance) + int(data['amount'])
                store.save()
                finance_serializer_ = FinanceSerializers(new_finance,many=False)
                return Response(finance_serializer_.data, status=status.HTTP_201_CREATED)
            else:
                return Response(finance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
            data = request.data['data']
            store=request.user.store
            finance=get_object_or_404(
            Finance, id=data['id'], store=store)
            if 'label_name' in data and data['label_name'] != '':
                label= FinanceLabel.objects.get_or_create(
                    name=data['label_name'],store=store)[0]
                finance.label = label
            diff_quantity=0
            if int(finance.amount) != int(data['amount']):
                diff_quantity = int(
                                    data['amount']) - int(finance.amount)
            finance_serializer = FinanceSerializers(finance,data=data)
            if finance_serializer.is_valid():
                finance_serializer.save()
                if data['type'] == 'Expense':
                    store.balance = int(store.balance) - diff_quantity
                elif data['type'] == 'Incomes':
                    store.balance = int(store.balance) + diff_quantity
                store.save()
                finance_serializer_ = FinanceSerializers(finance,many=False)

                return Response(finance_serializer_.data, status=status.HTTP_201_CREATED)
            else:
                return Response(finance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = request.GET['finance_id']
        store = request.user.store
        finance = get_object_or_404(
            Finance, id=id, store=store)
        finance_serializer = FinanceSerializers(finance, many=False)
        return Response(finance_serializer.data, status=status.HTTP_200_OK)


class Labels(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        store = request.user.store
        labels = FinanceLabel.objects.filter(store=store).order_by('name')
        labels_serializer = FinanceLabelSerializers(labels, many=True)
        return Response(labels_serializer.data, status=status.HTTP_200_OK)



class FinanceReport(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        store=request.user.store
        type = request.GET['type']
        month = request.GET['month']
      
        finances = list(Finance.objects.filter(store=store,type__icontains=type,date__icontains=month).annotate(dates=Count(
            'date')).values('dates').annotate(price=Sum('amount')).values('dates', 'price').order_by('dates'))

        return Response(finances, status=status.HTTP_200_OK)

class FinanceReport(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        store=request.user.store
        type = request.GET['type']
        month = request.GET['month']
      
        finances = list(Finance.objects.filter(store=store,type__icontains=type,date__icontains=month).annotate(dates=Count(
            'date')).values('dates').annotate(price=Sum('amount')).values('dates', 'price').order_by('dates'))

        return Response(finances, status=status.HTTP_200_OK)



class RemoveMultiFinance(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
            data = request.data['data']
            store = request.user.store
            for id in data:
                    finance=get_object_or_404(
                Finance, id=id, store=store)
                    if finance.type == 'Expense':
                        store.balance = int(store.balance) + int(finance.amount)
                    elif finance.type == 'Incomes':
                        store.balance = int(store.balance) - int(finance.amount)
                    store.save()
                    finance.delete()
            return Response('Success', status=status.HTTP_200_OK)
