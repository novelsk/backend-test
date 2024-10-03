from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel, models


class BaseProduct(TimestampedModel):
    """
    That is a base model for items and products.

    All fields here will be synchronized between items and related products.
    """

    AUTOSYNC_FIELDS = ["name", "ean", "unit"]

    name = models.CharField(_("Name"), max_length=255, db_index=True)
    ean = models.CharField(
        _("EAN"), max_length=13, blank=True, null=True, db_index=True
    )
    unit = models.CharField(
        _("Measurement Unit"),
        max_length=20,
        default="unit",
    )

    class Meta:
        abstract = True
