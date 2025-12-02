from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from payments.models import Payment
from payments.serializers import (
    PaymentListSerializer,
    PaymentRetrieveSerializer,
)


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):

    serializer_class = PaymentListSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list" and not self.request.user.is_staff:
            queryset = Payment.objects.filter(borrowing__user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        return PaymentRetrieveSerializer
