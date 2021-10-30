import uuid

from core.structures.store.models import Product, Order, Cart, OrderItem
from core.libs.managers.cart import CartManager
from core.libs.managers.product import ProductManager
from core.libs.lock_db import lock_db


class OrderManager:
    cart_manager = CartManager()
    product_manager = ProductManager()

    def get_queryset(self):
        return Order.objects.filter()

    def get_ordered_product(self, product_id):
        pass

    def generate_order_number(self, customer_id):
        random = str(uuid.uuid4())
        number = f"ODR-{random[-4:]}-CSTM{customer_id}"

        return number

    def add_order(self, customer_id):
        """
        Lock object every thread
        """

        # get cart by customer_id
        with lock_db('lock_when_order'):
            carts = self.cart_manager.get_cart_by_customer(customer_id)
            if not carts.exists():
                raise Exception("Cart is empty")

            # create order
            order = Order.objects.create(
                order_number=self.generate_order_number(customer_id),
                customer_id=customer_id,
                status=1,
            )

            # check product stock still available
            for cart in carts:
                product = cart.product
                product_available = self.product_manager.is_product_available(
                    product.id, cart.qty
                )
                if not product_available:
                    raise Exception(f"Out of stock.")

                # add product to order item
                OrderItem.objects.create(product=product, qty=cart.qty, order=order)

                # after create order item then remove product from cart and update qty product
                new_stock = product.stock - cart.qty
                self.product_manager.update_product(product.id, {"stock": new_stock})
                cart.delete()
