from rest_framework import serializers

from marketplace.models import Listing

from .marketplaces import SimpleMarketplaceSerializer


class DetailedListingSerializer(serializers.ModelSerializer):
    marketplace = SimpleMarketplaceSerializer()
    items_count = serializers.IntegerField(source="marketplace_items.count")

    class Meta:
        model = Listing
        fields = ["id", "name", "marketplace", "items_count"]


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ["id", "name", "marketplace_id"]
