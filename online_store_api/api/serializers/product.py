from re import S
from rest_framework import serializers
from core.structures.store.models import Product, OrderItem

WRITABLE_FIELDS = ("name", "stock")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id",) + WRITABLE_FIELDS


class ProductWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = WRITABLE_FIELDS + ("id",)


class ProductLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name")


class ProductSoldSerialiser(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate(self, attrs):
        data = super().validate(attrs)
        product = Product.objects.filter(id=data.get("product_id")).last()

        if not product:
            raise serializers.ValidationError({"product_id": "product not found"})

        return data
