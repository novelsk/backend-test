from rest_framework import serializers

from inventory.models import InventoryItem
from marketplace.api.serializers import ListingSerializer
from marketplace.models import Listing
from warehouse.api.serializers import WarehouseItemSerializer

from .owners import SimpleInventoryOwnerSerializer


class InventoryItemSerializer(serializers.ModelSerializer):
    owner = SimpleInventoryOwnerSerializer()
    gmid = serializers.CharField(source="product_id")
    warehouse_items = WarehouseItemSerializer(many=True)
    warehouse_total_stock = serializers.DecimalField(max_digits=12, decimal_places=2)
    listings = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "owner",
            "gmid",
            "name",
            "sku",
            "ean",
            "unit",
            "warehouse_items",
            "warehouse_total_stock",
            "listings",
        ]

    def get_listings(self, instance):
        if not instance.product_id:
            return []

        listings = Listing.objects.filter(
            marketplace_items__product_id=instance.product_id
        ).distinct()
        return ListingSerializer(listings, many=True).data


class SimpleInventoryItemSerializer(serializers.ModelSerializer):
    gmid = serializers.CharField(source="product_id")

    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "gmid",
            "name",
            "sku",
            "ean",
            "unit",
        ]
