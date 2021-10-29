from django.shortcuts import get_list_or_404, get_object_or_404
from core.structures.store.models import Cart


class CartManager:
    def get_queryset(self):
        return Cart.objects.filter()

    def get_cart_by_customer(self, customer_id):
        return self.get_queryset().filter(customer_id=customer_id)

    def get_cart_by_id(self, id):
        return self.get_queryset().filter(id=id)

    def get_or_404(self, id):
        return get_object_or_404(self.get_queryset(), id=id)

    def add_to_cart(self, data):
        product = data.get("product")
        customer = data.get("customer")
        qty = data.get("qty")

        # check cart with same costumer and product
        exists_cart = (
            self.get_queryset().filter(product=product, customer=customer).last()
        )
        if exists_cart:
            exists_cart.qty += qty
            exists_cart.save()
        else:
            exists_cart = Cart.objects.create(**data)
        return exists_cart

    def delete_or_404(self, product_id, customer_id):
        instances = get_list_or_404(
            self.get_queryset(), product_id=product_id, customer_id=customer_id
        )

        return self.get_queryset().filter(id__in=[i.id for i in instances]).delete()
