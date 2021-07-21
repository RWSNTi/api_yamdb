from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     DestroyAPIView)

from rest_framework.permissions import IsAdminUser
from .permissions import ReadOnly
# from apps.account.permissions import IsAdminPermission, ReadOnlyPermission из Эталонного кода

from .filters import TitleFilterBackend
from .models import Category, Genre, Title
from .serializers import (CategorySerializer, TitleSerializer,
                          GenreSerializer, TitleCreateSerializer)


class CommonListAPIView(ListCreateAPIView):
    permission_classes = [IsAdminUser | ReadOnly]  # [IsAdminPermission | ReadOnlyPermission]
    filter_backends = [SearchFilter]
    search_fields = ('name',)


class CategoriesListAPIView(CommonListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoriesDetailAPIView(DestroyAPIView):
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs['slug'])


class GenreListAPIView(CommonListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class GenreDetailAPIView(DestroyAPIView):
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Genre, slug=self.kwargs['slug'])


class TitleListAPIView(ListCreateAPIView):
    permission_classes = [IsAdminUser | ReadOnly]
    queryset = Title.objects.all()
    filter_backends = [TitleFilterBackend]

    def get_serializer_class(self):
        return TitleCreateSerializer if self.request.method == 'POST' else TitleSerializer


class TitleDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ReadOnly]
    queryset = Title.objects.all()

    def get_serializer_class(self):
        return TitleCreateSerializer if self.request.method in ['PATCH', 'PUT'] else TitleSerializer
