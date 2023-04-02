from django.contrib import admin
from .models import Account,UserOTP
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display= ('email','first_name','username','last_name','date_joined','is_active','last_login')
    list_display_links=('email','first_name','last_name')
    readonly_fields=('last_login','date_joined')
    ordering=('-date_joined',)


    filter_horizontal=()
    list_filter=()
    fieldsets=()


admin.site.register(Account,AccountAdmin)
admin.site.register(UserOTP)