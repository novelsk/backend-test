from typing import List

from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from inventory.models import InventoryItem

from .base_actions import BaseItemActionView


class Item2ItemBinderView(BaseItemActionView):
    """Binds item with another items!"""

    action_arg_name = "item_to_bind_id"

    @cached_property
    def item_to_bind_with(self) -> InventoryItem:
        return get_object_or_404(self.item_qs, pk=self.action_arg)

    def make_action(self) -> List[InventoryItem]:
        self.item.binder.bind_with_item(self.item_to_bind_with)

        return list(
            self.item_qs.filter(pk__in=[self.item.id, self.item_to_bind_with.id])
        )


class Item2NewBinderView(BaseItemActionView):
    """Binds item with new product!"""

    def make_action(self) -> List[InventoryItem]:
        self.item.binder.bind_with_new()

        return list(self.item_qs.filter(pk__in=[self.item.id]))
