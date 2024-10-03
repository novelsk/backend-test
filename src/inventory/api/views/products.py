from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from inventory.api.serializers import DetailedProductSerializer, UpdateProductSerializer
from inventory.models import Product


class ProductsView(RetrieveUpdateAPIView):
    """
    Get and update the product.

    This thing would be totally rewritten!
    """

    serializer_class = UpdateProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DetailedProductSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = DetailedProductSerializer(self.get_object()).data
        return response

    def perform_update(self, serializer):
        if serializer.validated_data:
            serializer.validated_data["autosync"] = False
        serializer.save()
