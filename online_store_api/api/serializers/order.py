from rest_framework import serializers
from core.structures.store.models import Order, Customer

from .product import ProductLiteSerializer


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, instance):
        serializer = ProductLiteSerializer(instance.products, many=True)
        return serializer.data

    class Meta:
        model = Order
        fields = ("id", "number", "status", "products")


class OrderWriteSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()

    def validate(self, attrs):
        customer_id = attrs.get("customer_id")
        customer = Customer.objects.filter(id=customer_id).last()
        if not customer:
            raise serializers.ValidationError({"customer_id": "Customer not found"})

        attrs["customer"] = customer
        return attrs
