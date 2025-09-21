from django.contrib import admin
from .models import User, Activity, Session, Booking, HydrationLog, ActivityLog, Reminder
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class UserAdminExt(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {'fields':('phone',)}),)

admin.site.register(Activity)
admin.site.register(Session)
admin.site.register(Booking)
admin.site.register(HydrationLog)
admin.site.register(ActivityLog)
admin.site.register(Reminder)
from django.db import transaction