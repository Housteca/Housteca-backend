from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

from common.ethereum import ETHEREUM_ADDRESS_REGEX


class Property(models.Model):
    city = models.CharField(max_length=128)
    country_code = models.CharField(max_length=4)
    risk = models.IntegerField(null=True, blank=True,
                               validators=[MaxValueValidator(100), MinValueValidator(0)])
    user = models.ForeignKey('users.User', on_delete=models.PROTECT)
    local_node = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='properties')
    contract_address = models.CharField(
        max_length=42,
        null=True,
        blank=True,
        unique=True,
        validators=[RegexValidator(regex=ETHEREUM_ADDRESS_REGEX,
                                   message='Invalid Ethereum address',
                                   code='nomatch')])

    class Meta:
        verbose_name_plural = 'Properties'

    def __str__(self) -> str:
        return f'{self.user.get_full_name()} - {self.city} ({self.country_code})'
