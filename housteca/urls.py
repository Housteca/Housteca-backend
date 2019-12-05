"""housteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Remove top-right corner link in django admin
admin.site.site_url = '/swagger'


info = openapi.Info(
    title='Housteca',
    default_version='v1',
    description="Housteca main backend service",
    contact=openapi.Contact(email="jmolinacolmenero@protonmail.com"),
    license=openapi.License(name="GNU v3.0"),
)

schema_view = get_schema_view(
    info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    re_path(r'^swagger/?$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    re_path(r'^redoc/?$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    path(r'api/', include([
        path('v1/', include([

        ])),
    ])),
]