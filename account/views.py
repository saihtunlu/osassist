from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from .models import User
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ChangePasswordSerializer, CustomTokenObtainPairSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from app.pagination import Pagination
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import update_last_login
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

from django.shortcuts import get_object_or_404
# Create your views here.
import random
import string


def key_generator():
    key = ''.join(random.choice(string.digits) for x in range(6))
    return key


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return key_generator


account_activation_token = TokenGenerator()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class Logout(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            black_listed_token, _ = BlacklistedToken.objects.get_or_create(
                token=token)
            black_listed_token.save()
        return Response('Success', status=status.HTTP_205_RESET_CONTENT)


class Auth(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        data = request.data['data']
        user = request.user
        user_serializer = UserSerializer(user, data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user_serializer = UserSerializer(request.user, many=False)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class Users(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        staffs = User.objects.filter(is_superuser=False)
        user_serializer = UserSerializer(staffs, many=True)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


def key_generator():
    key = ''.join(random.choice(string.digits) for x in range(6))
    if User.objects.filter(digit_token=key).exists():
        key = key_generator()
    return key


class VerifyCode(generics.ListAPIView):
    def post(self, request, *args, **kwargs):

        code = request.data["code"]
        uid = request.data["uid"]
        try:
            user = User.objects.get(pk=uid, digit_token=code)
            user.digit_token = ''
            user.save()
            return Response({'detail': 'Valid code!', 'uid': user.id, 'token': account_activation_token.make_token(user)}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Invalid code!'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(generics.ListAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        try:
            user = User.objects.get(email=email)
        except:
            return Response({'detail': 'Email you entered is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
        mail_subject = 'Reset password'
        token = key_generator()
        user.digit_token = token
        user.save()
        html_message = render_to_string('email/forgot.html', {
            'user': user,
            'token': token,
        })
        send_mail(mail_subject, html_message, 'saihtunlu14996@gmail.com',
                  [email], html_message=html_message)
        return Response({'detail': 'Password reset sent!', 'uid': user.id}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        uid = request.data['uid']
        token = request.data['token']
        password = request.data['password']
        try:
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({'detail': 'Reset password success. Now you can login your account.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Reset password link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(
            data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.update(instance=user,
                              validated_data={'password': request.data['password']})
            return Response('Changed!', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeEmail(generics.ListAPIView):
    def post(self, request, *args, **kwargs):

        email = request.data["email"]
        user = request.user
        mail_subject = 'Activate your email.'
        html_message = render_to_string('email/activation.html', {
            'user': user,
            'token': key_generator(),
        })
        send_mail(mail_subject, html_message, 'saihtunlu14996@gmail.com',
                  [email], html_message=html_message)
        return Response('Please confirm your email address to complete the registration', status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        uidb64 = request.data['uid']
        token = request.data['token']
        email = request.data['email']
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.email = email
            user.save()
            return Response({'detail': 'Thank you for your email confirmation. Now you can login your account.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
