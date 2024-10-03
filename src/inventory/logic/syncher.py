from typing import TYPE_CHECKING, Optional

from django.utils.functional import cached_property

if TYPE_CHECKING:
    from inventory.models import InventoryItem, Product


class ProductSyncher:
    def __init__(self, product: "Product"):
        self.product = product

    def sync(self):
        if not self.is_allowed_to_sync():
            return  # Raise here exception if you want

        for field in self.product.AUTOSYNC_FIELDS:
            setattr(self.product, field, getattr(self.item_to_sync_with, field))

        self.product.save()

    def is_allowed_to_sync(self) -> bool:
        return self.product.autosync and self.item_to_sync_with is not None

    @cached_property
    def item_to_sync_with(self) -> Optional["InventoryItem"]:
        return self.product.autosync_item
