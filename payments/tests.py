from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest import mock


SUCCESS_URL = reverse("payment:success")
CANCEL_URL = reverse("payment:cancel")


class PaymentTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @mock.patch("payments.views.stripe.checkout.Session.retrieve")
    def test_payment_success_return_200(self, mock_retrieve):
        session = mock.MagicMock()
        session.customer = "cus_123"
        session.__getitem__.return_value = {"metadata": {"type_of_payment": None}}
        mock_retrieve.return_value = session
        response = self.client.get(SUCCESS_URL, {"session_id": "test_session_id"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @mock.patch("payments.views.stripe.checkout.Session.retrieve")
    def test_payment_cancel_return_200(self, mock_retrieve):
        session = mock.MagicMock()
        session.customer = "cus_123"
        mock_retrieve.return_value = session
        response = self.client.get(CANCEL_URL, {"session_id": "test_session_id"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
