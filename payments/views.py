import stripe
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from payments.models import Payment
from payments.payment_services import set_status_paid, set_type_fine
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


@api_view(["GET"])
def success(request: HttpRequest) -> HttpResponse:
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)
    customer = session.customer
    type_of_payment = session["metadata"].get("type_of_payment")
    if type_of_payment == "pending":
        set_status_paid(session_id)
    elif type_of_payment == "fine":
        set_type_fine(session_id)
    return render(request, "success.html", {"customer": customer})


@api_view(["GET"])
def cancel(request: HttpRequest) -> HttpResponse:
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)
    customer = session.customer
    return render(request, "cancel.html", {"customer": customer})
