from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from book.models import Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.book_data = {
            "title": "Test Book 1",
            "author": "Author 1",
            "isbn": "1234567890123",
            "publication_date": "2023-01-01"
        }

        self.client.post(
            reverse('book-list'),
            self.book_data,
            format='json'
        )

        self.valid_payload = {
            "title": "New Test Book",
            "author": "Author 3",
            "isbn": "1112223334445",
            "publication_date": "2024-01-01"
        }
        self.invalid_payload = {
            "title": "",
            "author": "Author 3",
            "isbn": "1112223334445",
            "publication_date": "2024-01-01"
        }

    def test_get_books_list(self):
        response = self.client.get(reverse('book-list-sql'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_book(self):
        book_id = Book.objects.first().id
        response = self.client.get(reverse('book-detail', kwargs={'pk': book_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book_data['title'])

    def test_create_valid_book(self):
        response = self.client.post(reverse('book-list'), self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_book(self):
        response = self.client.post(reverse('book-list'), self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book(self):
        book_id = Book.objects.first().id
        update_payload = {
            "title": "Updated Test Book",
            "author": "Updated Author",
            "isbn": "1234567890123",
            "publication_date": "2023-01-01"
        }
        response = self.client.put(
            reverse('book-detail', kwargs={'pk': book_id}),
            update_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.get(id=book_id)
        self.assertEqual(book.title, "Updated Test Book")

    def test_delete_book(self):
        book_id = Book.objects.first().id
        response = self.client.delete(reverse('book-detail', kwargs={'pk': book_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
