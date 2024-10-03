from rest_framework.viewsets import ReadOnlyModelViewSet

from app.permissions import MarketplaceOnly, StuffAndSuperUserOnly
from marketplace.api.serializers import DetailedListingSerializer
from marketplace.models import Listing


class ListingViewSet(ReadOnlyModelViewSet):
    queryset = Listing.objects.order_by("id").select_related("marketplace")
    serializer_class = DetailedListingSerializer
    permission_classes = [StuffAndSuperUserOnly | MarketplaceOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.marketplace:
            qs = qs.filter(marketplace=self.request.marketplace)

        return qs
