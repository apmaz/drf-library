from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from borrow.models import Borrow
from book.serializers import BookSerializer
from notifications.telegram_services import send_borrow_created_message
from payments.payment_services import (
    create_checkout_session,
    total_amount,
    calculate_fine_amount,
)
from user.serializers import UserSerializer
from payments.serializers import PaymentListSerializer, PaymentShortSerializer


class BorrowListSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)
    user = serializers.SlugRelatedField(
        slug_field="email",
        read_only=True,
    )
    payments = PaymentShortSerializer(read_only=True, many=True)

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
            "payments",
        )


class BorrowRetrieveSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    payments = PaymentListSerializer(read_only=True, many=True)

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
            "payments",
        )


class BorrowSerializer(serializers.ModelSerializer):

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
            "actual_return_date",
            "user",
            "is_active",
        )

    def create(self, validated_data):
        book = validated_data["book"]
        request = self.context.get("request")
        with transaction.atomic():
            book.decrease_on_1_for_inventory()
            instance = Borrow.objects.create(**validated_data)
        send_borrow_created_message(instance)
        create_checkout_session(
            instance, request, type_of_payment="pending", amount_to_pay=total_amount
        )
        return instance


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
