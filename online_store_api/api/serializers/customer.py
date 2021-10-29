from rest_framework import serializers
from core.structures.store.models import Customer


class CustomerCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        username = data.get("username")
        exists_customer = Customer.objects.filter(username=username)
        if exists_customer.exists():
            raise serializers.ValidationError({"username": "Username already exists"})
        return data

    class Meta:
        model = Customer
        fields = (
            "id",
            "username",
        )


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "username")
