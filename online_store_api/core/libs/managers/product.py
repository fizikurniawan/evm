from rest_framework.generics import get_object_or_404
from django.db import transaction, models
from core.structures.store.models import Product, OrderItem


class ProductManager:
    def get_queryset(self):
        return Product.objects.filter()

    def add_product(self, data):
        return Product.objects.create(**data)

    def update_product(self, id, data):
        return Product.objects.filter(id=id).update(**data)

    def get_by_id(self, id):
        return self.get_queryset().filter(id=id).last()

    def get_or_404(self, id):
        return get_object_or_404(self.get_queryset(), id=id)

    def delete_product_or_404(self, id):
        instance = self.get_or_404(id)
        return instance.delete()

    def is_product_available(self, id, stock):
        instance = (
            self.get_queryset().filter(id=id, stock__gte=stock)
        )
        if not instance.exists():
            return False
        return True

    def get_ordered_product(self, id):
        return OrderItem.objects.filter(product_id=id).aggregate(models.Sum("qty"))[
            "qty__sum"
        ]
