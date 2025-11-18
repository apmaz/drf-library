from rest_framework import serializers
from borrow.models import Borrow
from book.serializers import BookSerializer
from user.serializers import UserSerializer


class BorrowListSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)
    user = serializers.SlugRelatedField(
        slug_field="email",
        read_only=True,
    )

    class Meta:
        model = Borrow
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
        )


class BorrowRetrieveSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Borrow
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
        )


class BorrowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrow
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )
