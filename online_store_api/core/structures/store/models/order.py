from django.db import models
from core.structures.store.models import Customer, Product

STATUS_CHOICES = ((1, "Pending"), (2, "Paid"), (3, "Canceled"))


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=25)
    status = models.IntegerField(choices=STATUS_CHOICES)
    issued_at = models.DateTimeField(auto_now_add=True)

    def get_items(self):
        return OrderItem.objects.filter(order=self)

    class meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()

    class meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
