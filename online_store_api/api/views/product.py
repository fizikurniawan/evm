from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.decorators import action

from ..serializers.product import (
    ProductSerializer,
    ProductWriteSerializer,
    ProductSoldSerialiser,
)

from core.libs.managers.product import ProductManager


class ProductViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    lookup_field = "id"
    product_manager = ProductManager()
    queryset = product_manager.get_queryset()

    def get_serializer_class(self):
        serializer_class = ProductSerializer
        if self.action in ["create", "update"]:
            serializer_class = ProductWriteSerializer
        if self.action == "get_total_product_ordered":
            serializer_class = ProductSoldSerialiser

        return serializer_class

    def update(self, request, id=None):
        self.product_manager.get_or_404(id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        self.product_manager.update_product(id, validated_data)

        return Response({"message": "Success update data", "data": validated_data})

    def destroy(self, request, id=None):
        self.product_manager.delete_product_or_404(id)

        return Response(
            {"message": "Success delete data"}, status=status.HTTP_204_NO_CONTENT
        )

    @action(methods=["POST"], detail=False, url_path="ordered")
    def get_total_product_ordered(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        product_id = validated_data.get("product_id")

        return Response(
            {
                "product_id": product_id,
                "total": self.product_manager.get_ordered_product(product_id),
                "current_stock": self.product_manager.get_by_id(product_id).stock
            }
        )
