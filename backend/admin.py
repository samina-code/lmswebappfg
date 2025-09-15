# backend/admin.py

from django.contrib import admin
from .models import (
    Student,
    Teacher,
    Semester,
    AssignedSubject,
    ContactMessage,
    ActivityLog,
)

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Semester)
admin.site.register(AssignedSubject)
admin.site.register(ContactMessage)
admin.site.register(ActivityLog)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "role", "is_active", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("role",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("role",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
