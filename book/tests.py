from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

from book.models import Book
from book.serializers import BookSerializer


BOOK_URL = reverse("book:book-list")


def get_book_url(book):
    return reverse("book:book-detail", args=[book.id])


class BaseBookAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.book_1 = Book.objects.create(
            title="Title_book_1",
            author="Author_book_1",
            cover="hard",
            inventory=3,
            daily_fee=10,
        )

        self.book_2 = Book.objects.create(
            title="Title_book_2",
            author="Author_book_2",
            cover="soft",
            inventory=3,
            daily_fee=10,
        )

        self.admin = get_user_model().objects.create_user(
            email="admin@test.com",
            password="password",
            is_staff=True,
        )

        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="password",
        )


class UnauthenticatedBookApiTest(BaseBookAPITest):
    def setUp(self):
        super().setUp()

    def test_unauthenticated_user_book_list_returns_200(self):
        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_unauthenticated_user_book_retrieve_returns_200(self):
        url = get_book_url(self.book_1)
        res = self.client.get(url)
        serializer = BookSerializer(self.book_1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_unauthenticated_user_cannot_create_book_returns_401(self):
        payload = {
            "title": "Title_book_payload",
            "author": "Author_book_payload",
            "cover": "hard",
            "inventory": 1,
            "daily_fee": 10,
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_patch_book_returns_401(self):
        url = get_book_url(self.book_1)
        payload = {
            "title": "Title_book_payload",
            "author": "Author_book_payload",
        }
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_put_book_returns_401(self):
        url = get_book_url(self.book_1)
        payload = {
            "title": "Title_book_payload",
            "author": "Author_book_payload",
            "cover": "hard",
            "inventory": 1,
            "daily_fee": 10,
        }
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_delete_book_returns_401(self):
        url = get_book_url(self.book_1)
        res = self.client.delete(url)
        self.assertTrue(Book.objects.filter(pk=self.book_1.id).exists())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTest(BaseBookAPITest):
    def setUp(self):
        super().setUp()

        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_book_list_returns_200(self):
        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_authenticated_user_book_retrieve_returns_200(self):
        url = get_book_url(self.book_1)
        res = self.client.get(url)
        serializer = BookSerializer(self.book_1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_authenticated_user_cannot_create_book_returns_403(self):
        payload = {
            "title": "Title_book_payload",
            "author": "Author_book_payload",
            "cover": "hard",
            "inventory": 1,
            "daily_fee": 10,
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_patch_book_returns_403(self):
        url = get_book_url(self.book_1)
        payload = {
            "title": "Title_book_payload",
            "author": "Author_book_payload",
        }
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_put_book_returns_403(self):
        url = get_book_url(self.book_1)
        payload = {
            "title": "Title_book_payload",
            "author": "Author_book_payload",
            "cover": "hard",
            "inventory": 1,
            "daily_fee": 10,
        }
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_delete_book_returns_403(self):
        url = get_book_url(self.book_1)
        res = self.client.delete(url)
        self.assertTrue(Book.objects.filter(pk=self.book_1.id).exists())
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTest(BaseBookAPITest):
    def setUp(self):
        super().setUp()

        self.client.force_authenticate(user=self.admin)

    def test_admin_user_book_list_returns_200(self):
        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_admin_user_book_retrieve_returns_200(self):
        url = get_book_url(self.book_1)
        res = self.client.get(url)
        serializer = BookSerializer(self.book_1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_admin_user_can_create_book_returns_201(self):
        payload = {
            "title": "Title_book_payload",
            "author": "Author_book_payload",
            "cover": "hard",
            "inventory": 1,
            "daily_fee": 10,
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_admin_user_can_patch_book_returns_201(self):
        url = get_book_url(self.book_1)
        payload = {
            "title": "Title_book_payload",
            "author": "Author_book_payload",
        }
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_user_can_put_book_returns_403(self):
        url = get_book_url(self.book_1)
        payload = {
            "title": "Title_book_payload",
            "author": "Author_book_payload",
            "cover": "hard",
            "inventory": 1,
            "daily_fee": 10,
        }
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_user_can_delete_book_returns_204(self):
        url = get_book_url(self.book_1)
        res = self.client.delete(url)
        self.assertFalse(Book.objects.filter(pk=self.book_1.id).exists())
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_create_duplicate_book_returns_400(self):
        payload = {
            "title": "Title_book_1",
            "author": "Author_book_1",
            "cover": "hard",
            "inventory": 3,
            "daily_fee": 10,
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
