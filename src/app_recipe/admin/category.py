from django.contrib import admin

from ..models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    search_fields = ("name", "slug")
    ordering = ("name",)
    list_per_page = 10
