from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response

from ..serializers.customer import CustomerSerializer, CustomerCreateSerializer
from core.structures.store.models import Customer


class CustomerViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    list:
        List all customer.

    List all customer.

    create:
        Create Customer.

    Create Customer.
    """

    queryset = Customer.objects.filter()

    def get_serializer_class(self):
        serializer_class = CustomerSerializer
        if self.action == "create":
            serializer_class = CustomerCreateSerializer

        return serializer_class
