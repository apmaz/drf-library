from rest_framework import serializers
from payments.models import Payment


class PaymentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "money_to_pay",
        )
