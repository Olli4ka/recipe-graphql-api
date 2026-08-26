from django.contrib import admin
from django.utils.html import format_html

from ..models import (
    Recipe,
    RecipeIngredient,
    Step,
)



class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class StepInline(admin.TabularInline):
    model = Step
    extra = 1



@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "image_preview",
        "image",
        "slug",
        "description",
        "cooking_time",
        "category",
        "author",
        "created_at",
        "updated_at",
    )

    list_display = (
        "id",
        "image_preview",
        "title",
        "slug",
        "category",
        "author",
        "cooking_time",

    )

    list_display_links = (
        "id",
        "title",
        "image_preview",
    )

    search_fields = (
        "title",
        "slug",
    )

    list_filter = (
        "category",
        "author__username",
        "created_at",
    )

    ordering = ("title",)

    list_per_page = 10

    autocomplete_fields = (
        "author",
        "category",
    )

    readonly_fields = (
        "image_preview",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    list_select_related = (
        "author",
        "category",
    )

    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 8px;" />',
                obj.image.url,
            )
        return "—"

    inlines = (
        RecipeIngredientInline,
        StepInline,
    )