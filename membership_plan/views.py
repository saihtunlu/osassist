from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import MembershipPlan
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import MembershipPlanSerializers
# Create your views here.


class Plans(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        plans = MembershipPlan.objects.all().order_by('id')
        plan_serializer = MembershipPlanSerializers(plans, many=True)
        return Response(plan_serializer.data, status=status.HTTP_200_OK)


class PlanView(APIView):

    def get(self, request, *args, **kwargs):
        id = request.GET['pid']
        plan = get_object_or_404(
            MembershipPlan, id=id)
        plan_serializer = MembershipPlanSerializers(plan, many=False)
        return Response(plan_serializer.data, status=status.HTTP_201_CREATED)
