import logging

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer

from common.authentication import extract_authorization_components, extract_address_from_authorization
from common.exceptions import APIException
from users.models import User
from users.serializers import UserSerializer


logger = logging.getLogger(__name__)


class UserCreateAPI(CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def perform_create(self, serializer: Serializer) -> None:
        try:
            message, signature = extract_authorization_components(self.request)
            address = extract_address_from_authorization(message, signature)
        except Exception:
            logger.exception('Failure processing credentials')
            raise APIException('Invalid credentials')
        if serializer.validated_data['address'] != address:
            raise ValidationError('Addresses do not match')
        serializer.save()


class UserRetrieveAPI(RetrieveAPIView):
    lookup_field = 'address'
    serializer_class = UserSerializer
    queryset = User.objects.all()
