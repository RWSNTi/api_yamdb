from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from titles.permissions import IsAdminAdmin
from .models import User, CHOICES
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
            except Exception:
                serializer.save(email=email_adr, username=email_adr,
                                role=CHOICES[0])
                print(serializer.data)
                user = get_object_or_404(User, email=email_adr)
                print(user.role)
                token = AccessToken().for_user(user)
                response = {'token': str(token)}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIGetUsers(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class APIGetUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminAdmin, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    lookup_field = 'username'
    filterset_fields = ['username', ]


class APIGetUpdateMeUser(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = self.request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid() and (
                'user' in user.role and user.is_staff is False):
            serializer.save(role=CHOICES[0])
            response = 'Вы можете изменить любые данные, кроме роли'
            return Response((response, serializer.data),
                            status=status.HTTP_200_OK)
        elif serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
