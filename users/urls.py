from django.urls import re_path

from users.views import UserCreateAPI, UserRetrieveAPI

urlpatterns = [
    re_path(r'^$', UserCreateAPI.as_view(), name='user_create_api'),
    re_path(r'^(?P<address>0x[0-9A-Fa-f]{40})/?$', UserRetrieveAPI.as_view(), name='user_retrieve_api'),
]
