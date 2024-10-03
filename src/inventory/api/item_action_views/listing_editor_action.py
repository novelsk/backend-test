from typing import List

from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from inventory.models import InventoryItem
from marketplace.models import Listing

from .base_actions import BaseItemActionView


class BaseListingEditorView(BaseItemActionView):
    action_arg_name = "listing_id"
    listing_qs = Listing.objects.all()

    @cached_property
    def listing(self) -> InventoryItem:
        return get_object_or_404(self.listing_qs, pk=self.action_arg)


class AddToListingView(BaseListingEditorView):
    """Add item to listing"""

    def make_action(self) -> List[InventoryItem]:
        self.item.listing_editor.add_to(self.listing)

        return list(self.item.product.inventory_items.all())


class RemoveFromListingView(BaseListingEditorView):
    """Remove item from listing"""

    def make_action(self) -> List[InventoryItem]:
        self.item.listing_editor.remove_from(self.listing)

        return list(self.item.product.inventory_items.all())
