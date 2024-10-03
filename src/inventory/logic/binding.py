from typing import TYPE_CHECKING

from django.apps import apps

from inventory import tasks
from inventory.logic.exceptions import ItemBindingException

if TYPE_CHECKING:
    from inventory.models import InventoryItem, Product


class ItemsBinder:
    def __init__(self, inventory_item: "InventoryItem"):
        self.inventory_item = inventory_item

    def bind_with_new(self):
        self._validate_new_binding()

        product = self._create_product()

        self.inventory_item.product = product
        self.inventory_item.save()

        self._call_sync(product)

    def bind_with_item(self, item_to_bind: "InventoryItem"):
        self._validate_item_binding(item_to_bind)

        product = (
            self.inventory_item.product
            or item_to_bind.product
            or self._create_product()
        )

        self.inventory_item.product = product
        item_to_bind.product = product

        # Save both for consistency
        self.inventory_item.save()
        item_to_bind.save()

        self._call_sync(product)

    def _validate_new_binding(self):
        if self.inventory_item.product:
            raise ItemBindingException("Already bind!")

    def _validate_item_binding(self, item_to_bind: "InventoryItem"):
        if self.inventory_item == item_to_bind:
            raise ItemBindingException("Impossible to bind to itself!")

        if self.inventory_item.owner_id == item_to_bind.owner_id:
            raise ItemBindingException("Impossible to bind items for the same owner!")

        if self.inventory_item.product and item_to_bind.product:
            raise ItemBindingException("Both products already have bindings!")

    def _create_product(self) -> "Product":
        Product = apps.get_model("inventory.Product")

        return Product.objects.create()

    def _call_sync(self, product: "Product"):
        tasks.sync_product_fields_with_related_items.delay(product.id)
