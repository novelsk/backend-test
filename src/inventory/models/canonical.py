from typing import TYPE_CHECKING, Optional

from django.utils.translation import gettext_lazy as _

from app.models import models
from inventory.logic.syncher import ProductSyncher

from .base import BaseProduct

if TYPE_CHECKING:
    from .items import InventoryItem


class Product(BaseProduct):
    """
    Canonical product with `gm-id` in it.
    """

    autosync = models.BooleanField(_("Autosync"), default=True)

    class Meta:
        verbose_name = _("Canonical product")
        verbose_name_plural = _("Canonical products")

    def __str__(self):
        return self.name

    @property
    def autosync_item(self) -> Optional["InventoryItem"]:
        """Here could be more complex logic - even maintainable FK to specified InventoryItem."""
        return self.inventory_items.first()

    @property
    def syncher(self):
        return ProductSyncher(self)
