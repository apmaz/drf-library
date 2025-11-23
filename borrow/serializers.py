from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
            "book",
        )

    def create(self, validated_data):
        book = validated_data["book"]
        book.decrease_on_1_for_inventory()
        return Borrow.objects.create(**validated_data)


class BorrowReturnSerializer(serializers.ModelSerializer):
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

        read_only_fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
        )

    def update(self, instance, validated_data):
        if not instance.is_active:
            raise ValidationError(
                {"This borrow": "Is unactive. You can't return this borrow twice"}
            )
        instance.is_active = False
        instance.actual_return_date = datetime.now().date()
        instance.book.increase_on_1_for_inventory()
        instance.save()
        return instance
