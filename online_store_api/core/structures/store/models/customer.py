from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=255)

    class meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
