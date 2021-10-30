from django.db import models

from .customer import Customer
from .product import Product
from .cart import Cart
from .order import Order, OrderItem


class LockDB(models.Model):
    lock_id = models.CharField(max_length=256, unique=True)
    creation_time = models.DateTimeField(auto_now_add=True)
