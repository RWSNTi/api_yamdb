from django.shortcuts import render
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404

from .models import User, RegistrationEmail
from .serializers import (RegEmailSerializer,
                          RegUserSerializer,
                          UserSerializer
                          )


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
            try:
                user = get_object_or_404(User, email=email_adr)
                token = AccessToken().for_user(user)
                response = {'access': str(token)}
            except status.HTTP_404_NOT_FOUND:
                serializer.save(email=email_adr, username=email_adr)
                user = get_object_or_404(User, email=email_adr)
                token = AccessToken().for_user(user)
                response = {'access': str(token)}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIGetUsers(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST) 
