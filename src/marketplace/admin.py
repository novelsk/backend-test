from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Listing, Marketplace


@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "slug",
    ]

    prepopulated_fields = {
        "slug": ["name"],
    }


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "marketplace",
        "region",
    ]

    list_display = [
        "name",
        "marketplace",
        "region",
        "marketplace_items_count",
    ]

    def marketplace_items_count(self, obj):
        if obj is not None:
            return obj.marketplace_items.count()

    marketplace_items_count.short_description = _("Marketplace items count")
