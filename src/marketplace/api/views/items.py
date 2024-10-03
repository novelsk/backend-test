from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from rest_framework.viewsets import ReadOnlyModelViewSet

from app.permissions import MarketplaceOnly, StuffAndSuperUserOnly
from marketplace.api.serializers import SimpleListingItemSerializer
from marketplace.models import Listing, MarketplaceItem


class ListingItemViewSet(ReadOnlyModelViewSet):
    queryset = MarketplaceItem.objects.select_related("product").order_by("id")
    serializer_class = SimpleListingItemSerializer
    permission_classes = [StuffAndSuperUserOnly | MarketplaceOnly]

    @cached_property
    def listing(self) -> Listing:
        filters = {"id": self.kwargs.get("listing_pk")}

        if self.request.marketplace:
            filters["marketplace"] = self.request.marketplace

        return get_object_or_404(Listing, **filters)

    def get_queryset(self):
        return super().get_queryset().filter(listings__id=self.listing.pk).distinct()
