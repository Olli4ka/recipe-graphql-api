from django.contrib import admin

from ..models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipe",
        "created_at",
    )

    list_display_links = (
        "id",
        "recipe",
    )

    search_fields = (
        "user__username",
        "recipe__title",
    )

    list_filter = ("created_at",)

    ordering = ("-created_at",)

    list_per_page = 10

    autocomplete_fields = (
        "user",
        "recipe",
    )

    readonly_fields = ("created_at",)

    date_hierarchy = "created_at"

    list_select_related = (
        "user",
        "recipe",
    )
