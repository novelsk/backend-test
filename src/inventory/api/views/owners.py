from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from inventory.api.serializers import InventoryOwnerSerializer
from inventory.models import InventoryOwner


class InventoryOwnersViewSet(ReadOnlyModelViewSet):
    queryset = InventoryOwner.objects.order_by("id").prefetch_related("warehouses")
    serializer_class = InventoryOwnerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"
