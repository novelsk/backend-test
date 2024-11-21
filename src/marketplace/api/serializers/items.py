from rest_framework import serializers

from marketplace.models import MarketplaceItem

from .products import MarketplaceProductSerializer


class SimpleListingItemSerializer(serializers.ModelSerializer):
    gmid = serializers.CharField(source="product_id")
    product = MarketplaceProductSerializer()
    wh_total_stock = serializers.DecimalField(
        source="total_stock", max_digits=10, decimal_places=2
    )
    wh_min_price = serializers.DecimalField(
        source="min_price", max_digits=10, decimal_places=2
    )
    wh_max_price = serializers.DecimalField(
        source="max_price", max_digits=10, decimal_places=2
    )

    class Meta:
        model = MarketplaceItem
        fields = [
            "id",
            "gmid",
            "status",
            "status_comment",
            "product",
            "wh_total_stock",
            "wh_min_price",
            "wh_max_price",
        ]
