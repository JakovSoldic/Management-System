from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Role, User, Subject, Enrollment

# Register your models here.
admin.site.register(Role)
admin.site.register(Subject)
admin.site.register(Enrollment)

@admin.register(User)
class Admin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('None', {'fields':('role', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('None', {'fields':('role', 'status')}),
    )
