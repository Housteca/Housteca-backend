from django.db.models import QuerySet, Q
from rest_framework.generics import ListAPIView

from properties.models import Property
from properties.serializers import PropertySerializer


class ListPropertyAPI(ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self) -> QuerySet:
        return Property.objects.filter(Q(user=self.request.user) | Q(local_node=self.request.user))
