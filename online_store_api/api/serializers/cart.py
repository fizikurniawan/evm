from rest_framework import serializers
from core.libs.managers.cart import CartManager
from core.structures.store.models import Cart, Customer, Product


class CartSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    def get_customer(self, instance):
        customer = instance.customer
        return {"id": customer.id, "username": customer.username}

    def get_product(self, instance):
        product = instance.product
        return {"id": product.id, "name": product.name}

    class Meta:
        model = Cart
        fields = ("id", "customer", "product", "qty")


class CartWriteSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    product_id = serializers.IntegerField()

    def validate(self, attrs):
        customer_id = attrs.get("customer_id")
        product_id = attrs.get("product_id")
        qty = attrs.get("qty")

        customer = Customer.objects.filter(id=customer_id).last()
        if not customer:
            raise serializers.ValidationError({"customer_id": "customer not found"})

        product = Product.objects.filter(id=product_id).last()
        if not product:
            raise serializers.ValidationError({"product_id": "product not found"})

        if qty < 1:
            raise serializers.ValidationError(
                {"qty": "quantity must be greather than equal 1"}
            )

        if product.stock < qty:
            raise serializers.ValidationError({"qty": "stock unavailable"})

        attrs["customer"] = customer
        attrs["product"] = product

        return attrs

    class Meta:
        model = Cart
        fields = ("customer_id", "product_id", "qty")


class CartRemoveSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    product_id = serializers.IntegerField()

    def validate(self, attrs):
        customer_id = attrs.get("customer_id")
        product_id = attrs.get("product_id")

        cart_manager = CartManager()
        cart = (
            cart_manager.get_queryset()
            .filter(customer_id=customer_id, product_id=product_id)
        )

        if not cart.exists():
            raise serializers.ValidationError({"cart": "cart not found"})

        return attrs
