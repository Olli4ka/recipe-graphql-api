from django.contrib import admin

from ..models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "recipe",
        "user",
        "rating",
        "created_at",
    )

    list_display_links = (
        "id",
        "recipe",
    )

    search_fields = (
        "recipe__title",
        "user__username",
        "comment",
    )

    list_filter = (
        "rating",
        "created_at",
    )

    ordering = ("-created_at",)

    list_per_page = 10

    autocomplete_fields = (
        "recipe",
        "user",
    )

    readonly_fields = ("created_at",)

    date_hierarchy = "created_at"

    list_select_related = (
        "recipe",
        "user",
    )
