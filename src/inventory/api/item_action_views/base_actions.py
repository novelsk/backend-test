from typing import List

from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from app.decorators import transform_exception
from app.views import LoginRequiredAPIView
from inventory.api.serializers import SimpleInventoryItemSerializer
from inventory.logic.exceptions import InventoryLogicException
from inventory.models import InventoryItem


class BaseItemActionView(LoginRequiredAPIView):
    item_qs = InventoryItem.objects.select_related("owner")
    serializer_class = SimpleInventoryItemSerializer

    action_arg_name = None

    def make_action(self) -> List[InventoryItem]:
        """Make here some action on `item` with `action_arg` and return affected item instances."""
        raise NotImplementedError()

    @cached_property
    def item(self) -> InventoryItem:
        return get_object_or_404(self.item_qs, pk=self.kwargs["item_id"])

    @cached_property
    def action_arg(self) -> InventoryItem:
        return self.kwargs.get(self.action_arg_name, None)

    def make_response(self, items: List[InventoryItem]) -> Response:
        return Response(
            {
                "affected_items": self.serializer_class(items, many=True).data,
            },
            status=status.HTTP_200_OK,
        )

    @transform_exception(InventoryLogicException, ValidationError)
    def post(self, request, *args, **kwargs):
        affected_items = self.make_action()
        return self.make_response(affected_items)
