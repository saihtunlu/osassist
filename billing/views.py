from membership_plan.models import MembershipPlan
from .models import Billing, BillingPayment, BillingImage, PaymentMethod
from store.models import Plan, Store
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import BillingPaymentSerializers, BillingSerializers, PaymentMethodSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from app.pagination import Pagination
import datetime


class BillingView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
            data = request.data['data']
            store = get_object_or_404(
                Store, id=data['store']['id'])
            selected_plan = get_object_or_404(
                MembershipPlan, id=data['selected_plan']['id'])
            billing = Billing(
                store=store,  selected_plan=selected_plan)
            del data['store']
            billing_serializer = BillingSerializers(billing, data=data)

            if billing_serializer.is_valid():
                billing_serializer.save()

                for payment in data['payments']:
                    payment_method = get_object_or_404(
                        PaymentMethod, id=payment['payment_method']['id'])
                    new_payment = BillingPayment(
                        payment_method=payment_method, billing=billing)
                    payment_serializer = BillingPaymentSerializers(
                        new_payment, data=payment)
                    if payment_serializer.is_valid():
                        payment_serializer.save()
                        for image in payment['images']:
                            new_payment_image = BillingImage(
                                billing_payment=new_payment)
                            new_payment_image.image = image['image']
                            new_payment_image.save()
                    else:
                        billing.delete()
                        return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(billing_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(billing_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
            data = request.data['data']
            store = request.user.store
            billing = get_object_or_404(
                Billing, id=data['id'], store=store)
            billing_serializer = BillingSerializers(billing, data=data)

            if billing_serializer.is_valid():
                billing_serializer.save()

                if len(data['payments']) > 0:
                    for payment in data['payments']:
                        if 'id' in payment:
                            payment_model = get_object_or_404(
                                BillingPayment, id=payment['id'])
                        else:
                            payment_model = BillingPayment(billing=billing)
                        payment_model.amount = payment['amount']
                        payment_model.date = payment['date']
                        payment_model.save()
                        if len(payment['images']) > 0:
                            BillingImage.objects.filter(
                                payment=payment_model).delete()
                            for image in payment['images']:
                                payment_model_image = BillingImage(
                                    payment=payment_model)
                                payment_model_image.image = image['image']
                                payment_model_image.save()

                return Response(billing_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(billing_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
            id = request.GET['bid']
            billing = get_object_or_404(
                Billing, id=id)
            billing_serializer = BillingSerializers(billing, many=False)
            return Response(billing_serializer.data, status=status.HTTP_200_OK)


class BillingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BillingSerializers
    pagination_class = Pagination

    def get_queryset(self):
        date = self.request.GET['date']
        order_by = self.request.GET['order_by']
        status = self.request.GET['status']

        store = self.request.user.store
        queryset = Billing.objects.filter(
            date__icontains=date, status__icontains=status, store=store).order_by(order_by)
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


class PaymentMethodsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
            methods = PaymentMethod.objects.all()
            methods_serializer = PaymentMethodSerializers(methods, many=True)
            return Response(methods_serializer.data, status=status.HTTP_200_OK)


class StoresBillingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BillingSerializers
    pagination_class = Pagination

    def get_queryset(self):
        date = self.request.GET['date']
        order_by = self.request.GET['order_by']
        status = self.request.GET['status']

        queryset = Billing.objects.filter(
            date__icontains=date, status__icontains=status).order_by(order_by)
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


class BillingPaymentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
            bid = request.data['bid']
            payment_status = request.data['payment_status']
            payment = request.data['payment']
            billing = get_object_or_404(
                Billing, id=bid)
            billing.payment_status = payment_status
            billing.save()

            payment_method = get_object_or_404(
                PaymentMethod, id=payment['payment_method']['id'])
            new_payment = BillingPayment(
                billing=billing, payment_method=payment_method)
            payment_serializer = BillingPaymentSerializers(
                new_payment, data=payment)
            if payment_serializer.is_valid():
                payment_serializer.save()
                for image in payment['images']:
                    new_payment_image = BillingImage(
                        billing_payment=new_payment)
                    new_payment_image.image = image['image']
                    new_payment_image.save()
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BillingStatusView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
            billing = request.data['data']
            status_ = request.data['status']
            store = get_object_or_404(
                Store, id=billing['store'])
            billing_ = get_object_or_404(
                Billing, id=billing['id'])
            billing_.status = status_
            billing_.save()

            if status_ == 'Active':
                plan = get_object_or_404(
                    Plan, store=store)
                if store.plan.plan.name == billing['selected_plan']['name']:

                    plan.exp_date = store.plan.exp_date + \
                        datetime.timedelta(
                            days=30*int(billing['number_of_months']))

                else:
                    membership_plan = MembershipPlan.objects.get(
                        id=billing['selected_plan']['id'])
                    plan.plan = membership_plan
                    plan.exp_date = datetime.now(
                    ) + datetime.timedelta(days=30*int(billing['number_of_months']))
                plan.save()
            return Response('Success', status=status.HTTP_201_CREATED)
