from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from inventory.api.serializers import InventoryItemSerializer
from inventory.models import InventoryItem


class InventoryItemMixin:
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = InventoryItem.objects.for_viewset()


class InventoryItemsViewSet(InventoryItemMixin, ReadOnlyModelViewSet):
    """List all items with filtering."""


class InventoryGroupedItemsView(InventoryItemMixin, ListAPIView):
    """List grouped items (10 per owner) with filtering."""

    pagination_class = None

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).group_by_owners()
