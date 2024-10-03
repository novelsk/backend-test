from rest_framework import serializers

from inventory.models import Product

from .items import SimpleInventoryItemSerializer


class DetailedProductSerializer(serializers.ModelSerializer):
    autosync_item = SimpleInventoryItemSerializer()
    inventory_items = SimpleInventoryItemSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "ean",
            "unit",
            "inventory_items",
            "autosync",
            "autosync_item",
        ]


class UpdateProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = [
            "name",
            "ean",
            "unit",
        ]
