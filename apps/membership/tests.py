from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from membership.models import Profile
from django.urls import reverse
from book.models import Book, BookEdition


class ProfileAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )

        self.profile = Profile.objects.create(
            user=self.user, role="Member"
        )

        self.profile_url = reverse('membership-list')
        self.detail_url = f"{self.profile_url}{self.profile.id}/"

        self.new_user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "newpassword"
        }
        self.new_profile_data = {
            "user": self.new_user_data,
            "role": "Member"
        }

    def test_create_profile(self):
        response = self.client.post(self.profile_url, self.new_profile_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["user"]["username"], self.new_user_data["username"])
        self.assertEqual(response.data["role"], self.new_profile_data["role"])

    def test_retrieve_profile(self):
        response = self.client.get(self.detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], self.user.username)
        self.assertEqual(response.data["role"], self.profile.role)

    def test_update_profile(self):
        update_data = {
            "user": {
                "username": "updateduser",
                "email": "updateduser@example.com",
                "first_name": "Updated",
                "last_name": "User"
            },
            "role": "Admin"
        }
        response = self.client.put(self.detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user.username, update_data["user"]["username"])
        self.assertEqual(self.profile.role, update_data["role"])

    def test_delete_profile(self):
        response = self.client.delete(self.detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(id=self.profile.id).exists())

    def test_profile_create_without_user(self):
        invalid_data = {"role": "Member"}
        response = self.client.post(self.profile_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_limit_error(self):
        from datetime import timedelta
        from django.utils.timezone import now
        for i in range(5):
            tmp = {
                "title": f"Test Book {i}",
                "author": f"Author {i}",
                "isbn": f"1234567890123_{i}",
                "publication_date": "2023-01-01"
            }
            book_obj = Book.objects.create(**tmp)
            book_edition_obj = BookEdition.objects.create(
                book=book_obj,
                edition_number=111,
                published_year=2024
            )

            self.profile.borrowrecord_set.create(
                book_edition=book_edition_obj,
                is_active=True,
                return_date=None,
                due_date=now() + timedelta(days=14)
            )
        result, detail = self.profile.check_booking_limit()
        self.assertFalse(result)
        self.assertEqual(detail, "max 5 kitap alabilirsiniz")

    def test_profile_overdue_error(self):
        from datetime import timedelta
        from django.utils.timezone import now
        tmp = {
            "title": f"Test Book",
            "author": f"Author",
            "isbn": f"123456789012",
            "publication_date": "2023-01-01"
        }
        book_obj = Book.objects.create(**tmp)
        book_edition_obj = BookEdition.objects.create(
            book=book_obj,
            edition_number=111,
            published_year=2024
        )

        self.profile.borrowrecord_set.create(
            book_edition=book_edition_obj,
            is_active=True, due_date=now() - timedelta(days=5), return_date=None
        )
        result, detail = self.profile.check_booking_borrowing()
        self.assertFalse(result)
        self.assertEqual(detail, "Geçikmede kitabnız var. yeni kitap alamazsınız")
