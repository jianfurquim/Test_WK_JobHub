from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("cpf", "name", "email", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    fieldsets = (
        (None, {"fields": ("cpf", "password")}),
        ("Informações Pessoais", {"fields": ("name", "email")}),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas Importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("cpf", "name", "email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("cpf", "name", "email")
    ordering = ("cpf",)


admin.site.register(User, CustomUserAdmin)
