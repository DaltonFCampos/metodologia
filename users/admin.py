from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Curso, Disciplina, Universidade, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin para o modelo customizado de usuários."""

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Informações pessoais",
            {"fields": ("name", "email", "city", "universidade", "curso")},
        ),
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
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "city",
                    "universidade",
                    "curso",
                ),
            },
        ),
    )
    list_display = (
        "username",
        "name",
        "email",
        "city",
        "universidade",
        "curso",
        "is_staff",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
        "universidade",
        "curso",
    )
    search_fields = ("username", "name", "email")
    ordering = ("username",)


@admin.register(Universidade)
class UniversidadeAdmin(admin.ModelAdmin):
    """Admin para universidades."""

    list_display = ("id", "nome", "polo")
    search_fields = ("nome", "polo")
    list_filter = ("polo",)
    ordering = ("nome",)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    """Admin para cursos."""

    list_display = ("id", "nome", "universidade")
    search_fields = ("nome", "universidade__nome")
    list_filter = ("universidade",)
    ordering = ("nome",)


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    """Admin para disciplinas."""

    list_display = ("id", "nome", "curso", "periodo")
    search_fields = ("nome", "curso__nome")
    list_filter = ("curso", "periodo")
    filter_horizontal = ("pre_requisitos",)
    ordering = ("curso", "periodo", "nome")
