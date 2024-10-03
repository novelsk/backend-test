from django.utils.translation import gettext_lazy as _

from app.models import SluggedModel, models


class InventoryOwner(SluggedModel):

    name = models.CharField(_("Name"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("Inventory owner")
        verbose_name_plural = _("Inventory owners")

    def __str__(self):
        return self.name
