from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from borrow.models import Borrow
from borrow.serializers import (
    BorrowListSerializer,
    BorrowRetrieveSerializer,
    BorrowSerializer,
    BorrowReturnSerializer,
)


class BorrowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Borrow.objects.all()
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def _params_to_ints(query_string):
        try:
            return [int(str_id) for str_id in query_string.split(',')]
        except ValueError:
            raise ValidationError(
                {
                    "user_id": "Must be an integer (ex. user_id=1)",
                }
            )

    @staticmethod
    def _params_to_bools(query_string):
        query_string = query_string.lower().strip()
        if query_string not in ("true", "false",):
            raise ValidationError(
                {
                    "is_active": "Must be 'true' or 'false' (ex. is_active=true or false)",
                }
            )
        if query_string == "true":
            return True
        return False

    def get_queryset(self):
        queryset = super().get_queryset()

        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if self.action =="list":
            if not self.request.user.is_staff:
                queryset = queryset.filter(user=self.request.user)
                if is_active:
                    is_active = self._params_to_bools(is_active)
                    queryset = queryset.filter(is_active=is_active)
                return queryset

            if self.request.user.is_staff:
                if user_id:
                    user_id = self._params_to_ints(user_id)
                    queryset = queryset.filter(user__id__in=user_id)
                if is_active:
                    is_active = self._params_to_bools(is_active)
                    queryset = queryset.filter(is_active=is_active)
                return queryset
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowListSerializer
        if self.action == "retrieve":
            return BorrowRetrieveSerializer
        if self.action == "return_of_borrow":
            return BorrowReturnSerializer
        return BorrowSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["POST",],
        detail=True,
        url_path="return"
    )
    def return_of_borrow(self, request, pk=None):
        borrow = self.get_object()
        serializer = self.get_serializer(borrow, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
