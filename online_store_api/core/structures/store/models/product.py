from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)

    class meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
