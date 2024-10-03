from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "owner",
        "region",
    ]
    list_display = [
        "name",
        "owner",
        "region",
        "warehouse_items_count",
    ]

    def warehouse_items_count(self, obj):
        if obj is not None:
            return obj.warehouse_items.count()

    warehouse_items_count.short_description = _("Warehouse items count")
