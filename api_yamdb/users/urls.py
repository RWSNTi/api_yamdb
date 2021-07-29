from django.urls import path

from .views import (APIRegEmail, APIRegUser,
                    APIGetUsers, APIGetUser,
                    APIGetUpdateMeUser)


urlpatterns = [
    path('v1/auth/mail', APIRegEmail.as_view(), name='reg_email'),
    path('v1/auth/token', APIRegUser.as_view(), name='reg_user'),
    path('v1/users/', APIGetUsers.as_view(), name='get_users'),
    path('v1/users/me/', APIGetUpdateMeUser.as_view(), name='get_me'),
    path('v1/users/<str:username>/', APIGetUser.as_view(), name='get_user'),
]
