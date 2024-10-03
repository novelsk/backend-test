from rest_framework import serializers

from inventory.models import Product


class MarketplaceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "ean",
            "unit",
            "autosync",
        ]
