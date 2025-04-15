from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OTP


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "role", "is_active", "is_verified")
    list_filter = ("role", "is_active", "is_superuser", "is_verified")
    search_fields = ("email",)
    ordering = ("email",)
    readonly_fields = (
        "last_login",
        "created_at",
        "updated_at",
        "is_staff",
        "is_superuser",
        "role",
        "email",
    )

    fieldsets = (
        (None, {"fields": ("email",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "is_verified",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("user", "otp", "expires_at", "generations")
    readonly_fields = ("user", "otp", "expires_at")
