from django.shortcuts import render
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, RegistrationEmail
from .serializers import RegEmailSerializer, RegUserSerializer


class APIRegEmail(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = RegEmailSerializer(data=request.data)
        if serializer.is_valid():
            code = get_random_string(length=6, allowed_chars='123456789')
            serializer.save(confirmation_code=code)
            address = self.request.data['email']
            send_mail('Код подтверждения для регистрации на YamDB',
                      f'Ваш код подтверждения - {code}, '
                      f'используйте его для получения токена',
                      'mailsender@yamdb.ru',
                      [address],
                      fail_silently=False,
                      )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIRegUser(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = RegUserSerializer(data=request.data)
        email_adr = self.request.data['email']
        if serializer.is_valid():
            serializer.save(email=email_adr, username=email_adr)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIGetUser(APIView):
    pass
