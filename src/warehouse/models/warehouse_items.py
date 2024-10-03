from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel, models


class WarehouseItem(TimestampedModel):
    """
    WarehouseItem with warehouse related data for InventoryItem:
        - stock
        - prices
    """

    inventory_item = models.ForeignKey(
        "inventory.InventoryItem",
        on_delete=models.CASCADE,
        related_name="warehouse_items",
    )
    warehouse = models.ForeignKey(
        "warehouse.Warehouse", on_delete=models.PROTECT, related_name="warehouse_items"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.DecimalField(_("Stock"), max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("Warehouse item")
        verbose_name_plural = _("Warehouse items")
        unique_together = ["inventory_item", "warehouse"]
