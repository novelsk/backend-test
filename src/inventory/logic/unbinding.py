from typing import TYPE_CHECKING

from inventory import tasks
from inventory.logic.exceptions import ItemBindingException

if TYPE_CHECKING:
    from inventory.models import InventoryItem, Product


class ItemsUnBinder:
    def __init__(self, inventory_item: "InventoryItem"):
        self.inventory_item = inventory_item

    def unbind_from_item(self, item_to_bind: "InventoryItem"):
        self._validate_item_unbinding(item_to_bind)

        bound_product = item_to_bind.product

        self.inventory_item.product = None
        self.inventory_item.save()

        self._call_sync(bound_product)

    def _validate_item_unbinding(self, item_to_bind: "InventoryItem"):
        if self.inventory_item == item_to_bind:
            raise ItemBindingException("Impossible to unbind from itself!")

        if (
            self.inventory_item.product != item_to_bind.product
            or self.inventory_item.product is None
            or item_to_bind.product is None
        ):
            raise ItemBindingException("Items were not bound together!")

    def _call_sync(self, product: "Product"):
        tasks.sync_product_fields_with_related_items.delay(product.id)
