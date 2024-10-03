from django.utils.translation import gettext_lazy as _

from app.models import SluggedModel, models


class Marketplace(SluggedModel):
    name = models.CharField(_("Name"), max_length=255, unique=True)

    user = models.ForeignKey("auth.User", null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Marketplace")
        verbose_name_plural = _("Marketplaces")

    def __str__(self):
        return self.name
