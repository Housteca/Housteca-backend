from django.urls import re_path

from users.views import UserCreateAPI

urlpatterns = [
    re_path('^$', UserCreateAPI.as_view(), name='user_create_api')
]
