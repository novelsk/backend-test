from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel, models


class MarketplaceItem(TimestampedModel):
    STATUS_CHOICES = (
        ("pending_confirmation", _("Pending confirmation")),
        ("confirmed", _("Confirmed")),
        ("declined", _("Declined")),
    )

    marketplace = models.ForeignKey(
        "marketplace.Marketplace",
        on_delete=models.PROTECT,
        related_name="marketplace_items",
    )
    product = models.ForeignKey(
        "inventory.Product",
        related_name="marketplace_items",
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        db_index=True,
        default="pending_confirmation",
    )
    status_comment = models.CharField(max_length=255, blank=True, null=True)
    external_id = models.CharField(
        _("External ID"), max_length=255, blank=True, null=True, db_index=True
    )

    listings = models.ManyToManyField(
        "marketplace.Listing", related_name="marketplace_items"
    )

    class Meta:
        verbose_name = _("Marketplace item")
        verbose_name_plural = _("Marketplace items")
        unique_together = (("marketplace", "product"), ("marketplace", "external_id"))

    def __str__(self):
        return f"{self.marketplace.name}: {self.product_id}"
