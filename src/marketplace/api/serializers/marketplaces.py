from rest_framework import serializers

from marketplace.models import Marketplace


class SimpleMarketplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketplace
        fields = ["id", "name", "slug"]
