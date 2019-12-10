from django.urls import re_path

from properties.views import ListPropertyAPI

urlpatterns = [
    re_path(r'^$', ListPropertyAPI.as_view(), name='list_property_api'),
]
