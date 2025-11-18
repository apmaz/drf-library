from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from borrow.models import Borrow
from borrow.serializers import (
    BorrowListSerializer,
    BorrowRetrieveSerializer,
    BorrowSerializer
)


class BorrowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Borrow.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowListSerializer
        if self.action == "retrieve":
            return BorrowRetrieveSerializer
        return BorrowSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
