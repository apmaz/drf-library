import datetime
import os
from unittest import mock

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from book.models import Book
from borrow.models import Borrow
from notifications.telegram_services import (
    send_borrow_created_message,
    send_borrow_overdue_message,
    send_borrow_not_overdue_message,
)


class SendMassageTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.book = Book.objects.create(
            title="Title_book_1",
            author="Author_book_1",
            cover="hard",
            inventory=3,
            daily_fee=10,
        )

        self.user = get_user_model().objects.create_user(
            email="user_1@user.com",
            password="password",
        )

        self.borrow = Borrow.objects.create(
            borrow_date=datetime.date(2025, 12, 16),
            expected_return_date=datetime.date(2025, 12, 18),
            book=self.book,
            user=self.user,
            is_active=True,
        )

    @mock.patch("notifications.telegram_services.requests.post")
    @mock.patch.dict(
        os.environ,
        {
            "BOT_TOKEN": "TEST_TOKEN",
            "TELEGRAM_CHAT_ID": "TEST_CHAT_ID",
        },
    )
    def test_send_borrow_created_message_func(self, mock_post):
        send_borrow_created_message(self.borrow)
        args, kwargs = mock_post.call_args
        mock_post.assert_called_once()
        assert args[0] == "https://api.telegram.org/botTEST_TOKEN/sendMessage"
        assert kwargs["json"]["chat_id"] == "TEST_CHAT_ID"
        assert f"Borrow ID: {self.borrow.id}," in kwargs["json"]["text"]
        assert f"Book ID: {self.borrow.book.id}," in kwargs["json"]["text"]
        assert f"User ID: {self.borrow.user.id}," in kwargs["json"]["text"]
        assert f"Created a new Borrow" in kwargs["json"]["text"]

    @mock.patch("notifications.telegram_services.requests.post")
    @mock.patch.dict(
        os.environ,
        {
            "BOT_TOKEN": "TEST_TOKEN",
            "TELEGRAM_CHAT_ID": "TEST_CHAT_ID",
        },
    )
    def test_send_borrow_overdue_message_func(self, mock_post):
        send_borrow_overdue_message(self.borrow)
        args, kwargs = mock_post.call_args
        mock_post.assert_called_once()
        assert args[0] == "https://api.telegram.org/botTEST_TOKEN/sendMessage"
        assert kwargs["json"]["chat_id"] == "TEST_CHAT_ID"
        assert f"Borrow ID: {self.borrow.id}," in kwargs["json"]["text"]
        assert f"Book ID: {self.borrow.book.id}," in kwargs["json"]["text"]
        assert f"User ID: {self.borrow.user.id}," in kwargs["json"]["text"]
        assert f"This Borrow is overdue:" in kwargs["json"]["text"]

    @mock.patch("notifications.telegram_services.requests.post")
    @mock.patch.dict(
        os.environ,
        {
            "BOT_TOKEN": "TEST_TOKEN",
            "TELEGRAM_CHAT_ID": "TEST_CHAT_ID",
        },
    )
    def test_send_borrow_not_overdue_message_func(self, mock_post):
        send_borrow_not_overdue_message()
        args, kwargs = mock_post.call_args
        mock_post.assert_called_once()
        assert args[0] == "https://api.telegram.org/botTEST_TOKEN/sendMessage"
        assert kwargs["json"]["chat_id"] == "TEST_CHAT_ID"
        assert f"There are no overdue borrowings today." in kwargs["json"]["text"]
