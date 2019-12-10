from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from documents.admin import DocumentInline
from users.models import User
from users.operations import is_investor, is_admin, is_local_node


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [DocumentInline]
    list_display = ('id', 'address_etherscan', 'first_name', 'last_name', 'email', 'is_investor', 'is_admin', 'is_local_node')
    search_fields = ('id', 'first_name', 'last_name', 'email', 'address')
    readonly_fields = ('date_joined',)

    def address_etherscan(self, obj: User) -> str:
        return format_html(f'<a target="_blank" href="{settings.ETHERSCAN_URI}/address/{obj.address}">{obj.address}</a>')

    address_etherscan.short_description = 'Address'
    address_etherscan.allow_tags = True

    def is_investor(self, obj: User) -> bool:
        return is_investor(obj.address)

    is_investor.boolean = True

    def is_admin(self, obj: User) -> bool:
        return is_admin(obj.address)

    is_admin.boolean = True

    def is_local_node(self, obj: User) -> bool:
        return is_local_node(obj.address)

    is_local_node.boolean = True
