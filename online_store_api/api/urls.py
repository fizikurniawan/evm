from django.conf.urls import url, include
from rest_framework import routers

from api.views.customer import CustomerViewSet
from api.views.product import ProductViewSet
from api.views.cart import CartViewSet
from api.views.order import OrderViewSet

router = routers.DefaultRouter()
router.register(r"customer", CustomerViewSet, "customer")
router.register(r"product", ProductViewSet, "product")
router.register(r"cart", CartViewSet, "cart")
router.register(r"order", OrderViewSet, "order")

urlpatterns = [
    url(r"", include(router.urls)),
]
