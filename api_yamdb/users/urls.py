from django.urls import path

from .views import APIRegEmail, APIRegUser


urlpatterns = [
    path('mail', APIRegEmail.as_view(), name='reg_email'),
    path('token', APIRegUser.as_view(), name='reg_user'),
    path('users', APIGetUser.as_view(), name='get_user'),
]
