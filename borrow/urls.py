from django.urls import path, include
from rest_framework import routers

from borrow.views import BorrowViewSet


app_name = "borrow"


router = routers.DefaultRouter()
router.register("borrows", BorrowViewSet, basename="borrow")

urlpatterns = [
    path("", include(router.urls)),
]
