import logging

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from core.libs.managers.order import OrderManager
from ..serializers.order import OrderSerializer, OrderWriteSerializer


class OrderViewSet(GenericViewSet):
    order_manager = OrderManager()

    def get_serializer_class(self):
        serializer_class = OrderSerializer
        if self.action == "create":
            serializer_class = OrderWriteSerializer

        return serializer_class

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        try:
            self.order_manager.add_order(validated_data.get("customer_id"))
        except Exception as err:
            logging.warning(str(err))
            return Response({"message": "Failed to add order"}, status=422)

        return Response({"message": "Success add cart to order"})
