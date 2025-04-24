from django.contrib import admin
from .models import CustomUser, SupportRequest, Message
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
##
# admin details: 
# username: admin1
# password: adminpass
# email:admin@mail.com
# #


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'staff_id']
    fieldsets = UserAdmin.fieldsets + (
        (_('Role Details'), {'fields': ('role', 'staff_id')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SupportRequest)
admin.site.register(Message)
