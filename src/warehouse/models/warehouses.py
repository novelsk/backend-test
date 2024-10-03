from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel, models


class Warehouse(TimestampedModel):
    """Owner warehouses."""

    name = models.CharField(_("Name"), max_length=255)
    owner = models.ForeignKey(
        "inventory.InventoryOwner", on_delete=models.PROTECT, related_name="warehouses"
    )
    region = models.ForeignKey(
        "regions.Region",
        on_delete=models.PROTECT,
        related_name="warehouses",
    )

    class Meta:
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")
        unique_together = ("name", "owner")

    def __str__(self):
        return f"{self.owner.name}: {self.name}"
