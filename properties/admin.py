from typing import Optional

from django import forms
from django.conf import settings
from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html

from documents.admin import DocumentInline
from properties.models import Property


class PropertyAdminForm(forms.ModelForm):
    def save(self, commit: bool = True) -> Property:
        if not self.instance.pk:
            self.instance.local_node = self.user
        return super().save(commit)

    class Meta:
        model = Property
        exclude = []


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    form = PropertyAdminForm
    inlines = [DocumentInline]
    list_display = ('id', 'contract_address_etherscan', 'country_code', 'city', 'risk', 'user', 'local_node')
    search_fields = ('id', 'contract_address', 'country_code', 'city', 'user__first_name', 'user__last_name',
                     'local_node__first_name', 'local_node__last_name')

    def get_form(self, request: HttpRequest, *args, **kwargs) -> forms.ModelForm:
        form = super().get_form(request, *args, **kwargs)
        form.user = request.user
        return form

    def contract_address_etherscan(self, obj: Property) -> Optional[str]:
        if not obj.contract_address:
            return None
        return format_html(
            f'<a target="_blank" href="{settings.ETHERSCAN_URI}/address/{obj.contract_address}">'
            f'{obj.contract_address or ""}</a>'
        )

    contract_address_etherscan.short_description = 'Contract address'
    contract_address_etherscan.allow_tags = True
