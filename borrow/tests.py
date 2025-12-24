import datetime
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from book.models import Book
from borrow.models import Borrow
from borrow.serializers import BorrowListSerializer, BorrowRetrieveSerializer

BORROW_URL = reverse("borrow:borrow-list")


def get_borrow_url(borrow):
    return reverse("borrow:borrow-detail", args=[borrow.id])


class BaseBorrowAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.book = Book.objects.create(
            title="Title_book_1",
            author="Author_book_1",
            cover="hard",
            inventory=3,
            daily_fee=10,
        )

        self.user_1 = get_user_model().objects.create_user(
            email="user_1@user.com",
            password="password",
        )

        self.user_2 = get_user_model().objects.create_user(
            email="user_2@user.com",
            password="password",
        )

        self.admin = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="password",
            is_staff=True,
        )

        self.borrow_1 = Borrow.objects.create(
            borrow_date=datetime.date(2025, 12, 16),
            expected_return_date=datetime.date(2025, 12, 18),
            book=self.book,
            user=self.user_1,
            is_active=False,
        )

        self.borrow_2 = Borrow.objects.create(
            borrow_date=datetime.date(2025, 12, 16),
            expected_return_date=datetime.date(2025, 12, 18),
            book=self.book,
            user=self.user_2,
            is_active=True,
        )

        self.borrow_3 = Borrow.objects.create(
            borrow_date=datetime.date(2025, 12, 16),
            expected_return_date=datetime.date(2025, 12, 18),
            book=self.book,
            user=self.admin,
            is_active=True,
        )

        self.borrow_4 = Borrow.objects.create(
            borrow_date=datetime.date(2025, 12, 16),
            expected_return_date=datetime.date(2025, 12, 18),
            book=self.book,
            user=self.user_2,
            is_active=True,
        )


class UnauthenticatedBorrowApiTest(BaseBorrowAPITest):
    def setUp(self):
        super().setUp()

    def test_unauthenticated_user_borrow_list_returns_401(self):
        res = self.client.get(BORROW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_borrow_retrieve_returns_401(self):
        url = get_borrow_url(self.borrow_1)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_create_borrow_returns_401(self):
        payload = {
            "borrow_date": datetime.date(2025, 12, 16),
            "expected_return_date": datetime.date(2025, 12, 18),
            "book": self.book.id,
            "user": self.user_1.id,
            "is_active": True,
        }
        res = self.client.post(BORROW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_patch_borrow_returns_401(self):
        url = get_borrow_url(self.borrow_1)
        payload = {
            "borrow_date": datetime.date(2025, 12, 17),
            "expected_return_date": datetime.date(2025, 12, 19),
        }
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_put_borrow_returns_401(self):
        url = get_borrow_url(self.borrow_1)
        payload = {
            "borrow_date": datetime.date(2025, 12, 16),
            "expected_return_date": datetime.date(2025, 12, 19),
            "book": self.book.id,
            "user": self.user_1.id,
            "is_active": True,
        }
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_delete_borrow_returns_401(self):
        url = get_borrow_url(self.borrow_1)

        res = self.client.delete(url)
        self.assertTrue(Borrow.objects.filter(pk=self.borrow_1.id).exists())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowApiTest(BaseBorrowAPITest):
    def setUp(self):
        super().setUp()

        self.client.force_authenticate(user=self.user_1)

    def test_authenticated_user_can_see_only_own_borrow_list_returns_200(self):
        res = self.client.get(BORROW_URL)
        borrows = Borrow.objects.all().filter(user=self.user_1.id)
        serializer = BorrowListSerializer(borrows, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_authenticated_user_borrow_retrieve_returns_200(self):
        url = get_borrow_url(self.borrow_1)
        res = self.client.get(url)
        serializer = BorrowRetrieveSerializer(self.borrow_1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_authenticated_user_can_create_borrow_returns_201(self):
        payload = {
            "borrow_date": datetime.date(2025, 12, 17),
            "expected_return_date": datetime.date(2025, 12, 18),
            "book": self.book.id,
            "user": self.user_1.id,
            "is_active": True,
        }
        res = self.client.post(BORROW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_cannot_patch_borrow_returns_405(self):
        url = get_borrow_url(self.borrow_1)
        payload = {
            "borrow_date": datetime.date(2025, 12, 17),
            "expected_return_date": datetime.date(2025, 12, 18),
        }
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authenticated_user_cannot_put_borrow_returns_405(self):
        url = get_borrow_url(self.borrow_1)
        payload = {
            "borrow_date": datetime.date(2025, 12, 17),
            "expected_return_date": datetime.date(2025, 12, 18),
            "book": self.book.id,
            "user": self.user_1.id,
            "is_active": True,
        }
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authenticated_user_cannot_delete_borrow_returns_405(self):
        url = get_borrow_url(self.borrow_1)

        res = self.client.delete(url)
        self.assertTrue(Borrow.objects.filter(pk=self.borrow_1.id).exists())
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AdminBorrowApiTest(BaseBorrowAPITest):
    def setUp(self):
        super().setUp()

        self.client.force_authenticate(user=self.admin)

    def test_admin_user_can_see_all_borrow_list_returns_200(self):
        res = self.client.get(BORROW_URL)
        borrows = Borrow.objects.all()
        serializer = BorrowListSerializer(borrows, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_admin_user_borrow_retrieve_returns_200(self):
        url = get_borrow_url(self.borrow_1)
        res = self.client.get(url)
        serializer = BorrowRetrieveSerializer(self.borrow_1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_admin_user_can_create_borrow_returns_201(self):
        payload = {
            "borrow_date": datetime.date(2025, 12, 18),
            "expected_return_date": datetime.date(2025, 12, 19),
            "book": self.book.id,
            "user": self.user_1.id,
            "is_active": True,
        }
        res = self.client.post(BORROW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_admin_user_cannot_patch_borrow_returns_405(self):
        url = get_borrow_url(self.borrow_1)
        payload = {
            "borrow_date": datetime.date(2025, 12, 18),
            "expected_return_date": datetime.date(2025, 12, 19),
        }
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_admin_user_cannot_put_borrow_returns_405(self):
        url = get_borrow_url(self.borrow_1)
        payload = {
            "borrow_date": datetime.date(2025, 12, 18),
            "expected_return_date": datetime.date(2025, 12, 18),
            "book": self.book.id,
            "user": self.user_1.id,
            "is_active": True,
        }
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_admin_user_cannot_delete_borrow_returns_405(self):
        url = get_borrow_url(self.borrow_1)

        res = self.client.delete(url)
        self.assertTrue(Borrow.objects.filter(pk=self.borrow_1.id).exists())
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_search_filter_borrow_by_user_id_returns_200(self):
        res = self.client.get(BORROW_URL, {"user_id": f"{self.user_2.id}"})
        serializer_without_search_user_1 = BorrowListSerializer(self.borrow_1)
        serializer_with_search_user_2 = BorrowListSerializer(self.borrow_2)
        serializer_without_search_user_3 = BorrowListSerializer(self.borrow_3)
        serializer_with_search_user_4 = BorrowListSerializer(self.borrow_4)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_with_search_user_2.data, res.data)
        self.assertIn(serializer_with_search_user_4.data, res.data)
        self.assertNotIn(serializer_without_search_user_1.data, res.data)
        self.assertNotIn(serializer_without_search_user_3.data, res.data)

    def test_search_filter_borrow_by_user_is_and_is_active_returns_200(self):
        res = self.client.get(BORROW_URL, {"is_active": f"true"})
        serializer_without_search_is_active_1 = BorrowListSerializer(self.borrow_1)
        serializer_with_search_is_active_2 = BorrowListSerializer(self.borrow_2)
        serializer_with_search_is_active_3 = BorrowListSerializer(self.borrow_3)
        serializer_with_search_is_active_4 = BorrowListSerializer(self.borrow_4)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_with_search_is_active_2.data, res.data)
        self.assertIn(serializer_with_search_is_active_3.data, res.data)
        self.assertIn(serializer_with_search_is_active_4.data, res.data)
        self.assertNotIn(serializer_without_search_is_active_1.data, res.data)

    def test_search_filter_borrow_by_is_active_returns_200(self):
        res = self.client.get(
            BORROW_URL, {"user_id": f"{self.user_1.id}", "is_active": "false"}
        )
        serializer_with_search_parameters_1 = BorrowListSerializer(self.borrow_1)
        serializer_without_search_parameters_2 = BorrowListSerializer(self.borrow_2)
        serializer_without_search_parameters_3 = BorrowListSerializer(self.borrow_3)
        serializer_without_search_parameters_4 = BorrowListSerializer(self.borrow_4)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_with_search_parameters_1.data, res.data)
        self.assertNotIn(serializer_without_search_parameters_2.data, res.data)
        self.assertNotIn(serializer_without_search_parameters_3.data, res.data)
        self.assertNotIn(serializer_without_search_parameters_4.data, res.data)
