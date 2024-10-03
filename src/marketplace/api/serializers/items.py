from rest_framework import serializers

from marketplace.models import MarketplaceItem

from .products import MarketplaceProductSerializer


class SimpleListingItemSerializer(serializers.ModelSerializer):
    gmid = serializers.CharField(source="product_id")
    product = MarketplaceProductSerializer()

    class Meta:
        model = MarketplaceItem
        fields = [
            "id",
            "gmid",
            "status",
            "status_comment",
            "product",
        ]
