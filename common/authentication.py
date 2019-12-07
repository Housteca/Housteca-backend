import base64
import binascii
from datetime import timedelta, datetime
from typing import Tuple, Optional, Any

from django.utils.dateparse import parse_datetime
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from web3.auto import w3

from users.models import User


class EthereumAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[User, Any]]:
        """
        Returns a `User` if the signature provided in the Authorization header is correct.
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'housteca':
            return None

        if len(auth) == 1:
            msg = 'Invalid housteca header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid housteca header. Credentials string should not contain spaces.')
            raise AuthenticationFailed(msg)

        try:
            auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = 'Invalid housteca header. Credentials not correctly base64 encoded.'
            raise AuthenticationFailed(msg)

        message, signature = auth_parts[0], auth_parts[2]
        return self.authenticate_credentials(message, signature)

    def authenticate_credentials(self, message: str, signature: str) -> Tuple[User, Any]:
        try:
            datetime_obj = parse_datetime(message)
        except ValueError:
            raise AuthenticationFailed('Not a valid datetime')
        now = datetime.utcnow()
        if now - timedelta(seconds=3) < datetime_obj < now + timedelta(seconds=3):
            address = w3.eth.account.recover_message(message, signature)
            try:
                user = User.objects.get(address__iexact=address)
            except User.DoesNotExist:
                raise AuthenticationFailed('Invalid user')
            return user, None
        raise AuthenticationFailed('Only three-second intervals are allowed')
