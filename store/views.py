from .models import Store,Plan,MembershipPlan
from account.models import User
from account.serializers import UserSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import StoreSerializers
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from app.pagination import Pagination


class Stores(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StoreSerializers
    pagination_class = Pagination

    def get_queryset(self):
        request = self.request
        queryset = Store.objects.filter(
            name__icontains=request.GET['query']).order_by(request.GET['order_by'])
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


class SingleStore(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        store = request.data['store']
        new_store = Store()
        store_serializer = StoreSerializers(new_store, data=store)
        if store_serializer.is_valid():
            store_serializer.save()
            return Response(store_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(store_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data['data']
        store = get_object_or_404(
            Store, id=data['id'])
        store_serializer = StoreSerializers(store, data=data)
        if store_serializer.is_valid():
            store_serializer.save()

            return Response(store_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(store_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        id = request.GET['sid']
        store = get_object_or_404(
            Store, id=id)
        store_serializer = StoreSerializers(store, many=False)
        return Response(store_serializer.data, status=status.HTTP_200_OK)


class RegisterStore(generics.ListAPIView):

    def post(self, request, *args, **kwargs):
        store = request.data['store']
        plan = request.data['plan']
        staff = request.data['staff']
        try:
            Store.objects.get(email=staff['email'])
            return Response({'details': "This store's email is already used!"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        new_store = Store()
        new_store.email = store['email']
        new_store.fbLink = store['fbLink']
        new_store.name = store['name']
        new_store.phone = store['phone']
        new_store.type = store['type']
        new_store.currency = store['settings']['currency']
        new_store.tax_type = store['settings']['tax_type']
        new_store.save()


        membership = MembershipPlan.objects.get(pk=plan['plan']['id'])
        plan_ = Plan(store=new_store, plan=membership)
        plan_.exp_date = plan['exp_date']
        plan_.free_trail_exp_date = plan['free_trail_exp_date']
        plan_.save()

    

        if staff['password'] != staff['password_confirm']:
            new_store.delete()
            return Response({'details': "Password and confirmation password do not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(email=staff['email'])
            new_store.delete()
            return Response({'details': 'This email is already used!'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        new_staff = User.objects.create_user(
            email=staff['email'],
            username=staff['username'],
            password=staff['password'],
            store=new_store
        )

        user_serializer = UserSerializer(new_staff, data=staff)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            new_store.delete()
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'details': 'Success'}, status=status.HTTP_201_CREATED)