from django.db import models

from .product import Product
from .customer import Customer


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
