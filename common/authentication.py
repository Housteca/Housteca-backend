import base64
import binascii
from datetime import timedelta, datetime
from typing import Tuple, Optional, Any

from django.utils import timezone
from django.utils.timezone import utc
from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from web3.auto import w3

from users.models import User


def extract_authorization_components(request: Request) -> Tuple[Optional[str], Optional[str]]:
    auth = get_authorization_header(request).split()

    if not auth or auth[0].lower() != b'housteca':
        return None, None

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

    return auth_parts[0], auth_parts[2]


def extract_address_from_authorization(message: str, signature: str) -> str:
    try:
        datetime_obj = datetime.fromtimestamp(float(message), tz=utc)
    except ValueError:
        raise AuthenticationFailed('Not a valid datetime')
    now = timezone.now()
    if now - timedelta(seconds=3) < datetime_obj < now + timedelta(seconds=3):
        encoded_message = encode_defunct(text=message)
        return w3.eth.account.recover_message(encoded_message, signature=signature)
    raise AuthenticationFailed('Only three-second intervals are allowed')


class EthereumAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[User, Any]]:
        """
        Returns a `User` if the signature provided in the Authorization header is correct.
        """
        message, signature = extract_authorization_components(request)
        if message is None or signature is None:
            return None
        return self.authenticate_credentials(message, signature)

    @staticmethod
    def authenticate_credentials(message: str, signature: str) -> Tuple[User, Any]:
        address = extract_address_from_authorization(message, signature)
        try:
            user = User.objects.get(address__iexact=address)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid user')
        return user, None
