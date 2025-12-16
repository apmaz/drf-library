from payments.views import success, cancel
from django.urls import path

app_name = "payment"

urlpatterns = [
    path("success/", success, name="success"),
    path("cancel/", cancel, name="cancel"),
]
