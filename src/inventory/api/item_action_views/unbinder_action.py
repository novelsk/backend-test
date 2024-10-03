from typing import List

from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from inventory.models import InventoryItem

from .base_actions import BaseItemActionView


class ItemFromItemUnBinderView(BaseItemActionView):
    """Unbinds one item from another!"""

    action_arg_name = "item_to_unbind_id"

    @cached_property
    def item_to_unbind_from(self) -> InventoryItem:
        return get_object_or_404(self.item_qs, pk=self.action_arg)

    def make_action(self) -> List[InventoryItem]:
        self.item.unbinder.unbind_from_item(self.item_to_unbind_from)

        return list(self.item_qs.filter(pk__in=[self.item.id]))
