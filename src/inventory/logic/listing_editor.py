from typing import TYPE_CHECKING

from django.apps import apps

from inventory.logic.exceptions import ListingEditingException

if TYPE_CHECKING:
    from inventory.models import InventoryItem
    from marketplace.models import Listing


class ListingEditor:
    def __init__(self, inventory_item: "InventoryItem"):
        self.inventory_item = inventory_item

    def add_to(self, listing: "Listing"):
        self._validate_add_to(listing)

        MarketplaceItem = apps.get_model("marketplace.MarketplaceItem")
        marketplace_item, _ = MarketplaceItem.objects.get_or_create(
            marketplace=listing.marketplace,
            product=self.inventory_item.product,
        )

        marketplace_item.listings.add(listing)

    def remove_from(self, listing: "Listing"):
        self._validate_remove_from(listing)

        MarketplaceItem = apps.get_model("marketplace.MarketplaceItem")
        marketplace_item, _ = MarketplaceItem.objects.get_or_create(
            marketplace=listing.marketplace,
            product=self.inventory_item.product,
        )

        marketplace_item.listings.remove(listing)

    def _validate_add_to(self, listing: "Listing"):
        product = self.inventory_item.product
        if not product:
            raise ListingEditingException("InventoryItem must be bound to product.")

        if listing.marketplace_items.filter(product=product).exists():
            raise ListingEditingException("Already in listing!")

    def _validate_remove_from(self, listing: "Listing"):
        product = self.inventory_item.product
        if not product:
            raise ListingEditingException("InventoryItem must be bound to product.")

        if not listing.marketplace_items.filter(product=product).exists():
            raise ListingEditingException("Nothing to remove!")
