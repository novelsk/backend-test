from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel, models


class Listing(TimestampedModel):
    """
    Listing is a named group of marketplace items for some region or store.

    Change marketplace`s OneToOneField to ForeignKey as soon as you need many
    stores, regions, feeds etc for one marketplace.
    """

    name = models.CharField(_("Name"), max_length=255)
    marketplace = models.OneToOneField(
        "marketplace.Marketplace",
        on_delete=models.PROTECT,
        related_name="listing",
        verbose_name=_("Marketplace"),
    )
    region = models.ForeignKey(
        "regions.Region",
        on_delete=models.PROTECT,
        related_name="listings",
    )

    class Meta:
        verbose_name = _("Listing")
        verbose_name_plural = _("Listings")
        unique_together = ("name", "marketplace")

    def __str__(self):
        return f"{self.marketplace.name}: {self.name}"
