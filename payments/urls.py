from django.urls import include
from rest_framework import routers

from payments.payment_services import success
from payments.views import PaymentViewSet
from django.urls import path

app_name = "payment"

router = routers.DefaultRouter()
router.register("payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path("success/", success, name="success"),
]
