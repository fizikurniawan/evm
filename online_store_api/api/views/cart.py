from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from core.libs.managers.cart import CartManager
from ..serializers.cart import CartSerializer, CartWriteSerializer, CartRemoveSerializer


class CartViewSet(GenericViewSet):
    lookup_field = "customer_id"
    cart_manager = CartManager()

    def get_serializer_class(self):
        serializer_class = CartSerializer
        if self.action == "create":
            serializer_class = CartWriteSerializer
        elif self.action == "remove_from_cart":
            serializer_class = CartRemoveSerializer

        return serializer_class

    def retrieve(self, request, customer_id=None):
        queryset = self.cart_manager.get_cart_by_customer(customer_id)
        serializer = self.get_serializer(queryset, many=True)

        return Response({"message": "sucess get cart", "data": serializer.data})

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        self.cart_manager.add_to_cart(validated_data)

        return Response({"message": "Success add to cart"})

    @action(methods=["POST"], detail=False, url_path="remove")
    def remove_from_cart(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        self.cart_manager.delete_or_404(**validated_data)

        return Response({"message": "success remove from cart"})
