from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date, timedelta
from book.models import Book
from membership.models import Profile
from borrow.models import BorrowRecord


class BorrowRecordAPITestCase(APITestCase):
    def setUp(self):
        self.profile = Profile.objects.create(user_id=1, role="Member")
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            isbn="1234567890123",
            publication_date="2023-01-01"
        )
        self.borrow_data = {
            "member": self.profile.id,
            "book": self.book.id,
            "borrow_date": date.today(),
            "due_date": date.today() + timedelta(days=14)
        }

        self.borrow_record = BorrowRecord.objects.create(
            member=self.profile,
            book=self.book,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14)
        )

    def test_get_borrow_records_list(self):
        response = self.client.get(reverse('borrow'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_borrow_record(self):
        response = self.client.get(
            reverse('borrow-detail', kwargs={'pk': self.borrow_record.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['member'], self.profile.id)

    def test_create_valid_borrow_record(self):
        response = self.client.post(reverse('borrow'), self.borrow_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_borrow_record(self):
        invalid_data = self.borrow_data.copy()
        invalid_data['due_date'] = date.today() - timedelta(days=1)
        response = self.client.post(reverse('borrow'), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_borrow_record(self):
        update_data = {
            "member": self.profile.id,
            "book": self.book.id,
            "borrow_date": date.today(),
            "due_date": date.today() + timedelta(days=21)
        }
        response = self.client.put(
            reverse('borrow-detail', kwargs={'pk': self.borrow_record.id}),
            update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrow_record = BorrowRecord.objects.get(id=self.borrow_record.id)
        self.assertEqual(borrow_record.due_date, date.today() + timedelta(days=21))

    def test_delete_all_borrow_record(self):
        for borrow_id in BorrowRecord.objects.filter().values("id"):
            response = self.client.delete(
                reverse('borrow-detail', kwargs={'pk': borrow_id["id"]})
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(BorrowRecord.objects.count(), 0) # tumu silinmis ise count 0 donmesi gerek
