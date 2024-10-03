from rest_framework.viewsets import ReadOnlyModelViewSet

from app.permissions import StuffAndSuperUserOnly
from marketplace.api.serializers import SimpleMarketplaceSerializer
from marketplace.models import Marketplace


class MarketplaceViewSet(ReadOnlyModelViewSet):
    queryset = Marketplace.objects.order_by("id")
    serializer_class = SimpleMarketplaceSerializer
    permission_classes = [StuffAndSuperUserOnly]
    lookup_field = "slug"
