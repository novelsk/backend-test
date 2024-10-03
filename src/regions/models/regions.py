from django.utils.translation import gettext_lazy as _

from app.models import SluggedModel, models


class Region(SluggedModel):
    """Region to group inventory and marketplace items by."""

    name = models.CharField(_("Name"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return self.name
