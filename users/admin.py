from django.contrib import admin

from users.models import User
from users.operations import is_investor, is_admin, is_local_node


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'address', 'is_investor', 'is_admin', 'is_local_node')
    readonly_fields = ('date_joined',)

    def is_investor(self, user: User) -> bool:
        return is_investor(user.address)

    is_investor.boolean = True

    def is_admin(self, user: User) -> bool:
        return is_admin(user.address)

    is_admin.boolean = True

    def is_local_node(self, user: User) -> bool:
        return is_local_node(user.address)

    is_local_node.boolean = True
