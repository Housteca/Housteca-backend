import base64
from datetime import datetime
from typing import Dict, Any

from django.test import TestCase
from eth_account.messages import encode_defunct

from common.ethereum import w3
from users.models import User


class BaseTestAPI(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.private_key = '0x962c914f5e53a426b64f32ed9415c923efe8a853c68747b70aa377c67a20a69e'
        self.user = User.objects.create_user('test', 'test@test.com',
                                             address='0x9d758cDFE97e0ecFa14ce8Fb1Dba315D1390fF7C')

    def credentials(self) -> Dict[str, Any]:
        credentials = self.build_credentials()
        return {'HTTP_AUTHORIZATION': f'Housteca {credentials}'}

    def build_credentials(self) -> str:
        timestamp = str(int(datetime.timestamp(datetime.utcnow())))
        signature = w3.eth.account.sign_message(
            encode_defunct(text=timestamp),
            private_key=self.private_key
        ).signature.hex()
        return base64.b64encode(f'{timestamp}:{signature}'.encode()).decode()
