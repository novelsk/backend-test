from django.contrib import admin

from .models import InventoryOwner


@admin.register(InventoryOwner)
class InventoryOwnerAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "slug",
    ]

    prepopulated_fields = {
        "slug": ["name"],
    }
