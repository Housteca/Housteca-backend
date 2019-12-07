from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from common.ethereum import ETHEREUM_ADDRESS_REGEX


class User(AbstractUser):
    address = models.CharField(
        max_length=42,
        unique=True,
        validators=[RegexValidator(regex=ETHEREUM_ADDRESS_REGEX,
                                   message='Invalid Ethereum address',
                                   code='nomatch')])

    def __str__(self) -> str:
        return self.address
