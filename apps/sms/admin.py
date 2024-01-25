from django.contrib import admin
from django.contrib.auth.models import User, Group
from solo.admin import SingletonModelAdmin
from .models import SmsSetting, SmsLog

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(SmsSetting)
class SmsSettingAdmin(SingletonModelAdmin):
    list_display = ('id', 'provider')


@admin.register(SmsLog)
class SmsLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'phone', 'message', 'is_send', 'created_at')
    list_display_links = ('id', 'provider')
    readonly_fields = ('id', 'provider', 'phone', 'message', 'content', 'is_send', 'created_at')
