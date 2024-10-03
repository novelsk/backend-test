from rest_framework import serializers

from warehouse.models import WarehouseItem


class WarehouseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseItem
        fields = ["id", "warehouse_id", "price", "stock"]
