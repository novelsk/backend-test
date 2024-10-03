from rest_framework import serializers

from inventory.models import InventoryOwner
from warehouse.api.serializers import WarehouseSerializer


class SimpleInventoryOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryOwner
        fields = ["id", "name", "slug"]


class InventoryOwnerSerializer(serializers.ModelSerializer):
    warehouses = WarehouseSerializer(many=True)

    class Meta:
        model = InventoryOwner
        fields = ["id", "name", "slug", "warehouses"]
