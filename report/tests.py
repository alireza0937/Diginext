from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class ReportingAPIViewTestCase(APITestCase):

    def setUp(self):
        ReportingAPIView.objects.create(title='Test Book 1', author='Author 1', published_date='2022-01-01')
        Book.objects.create(title='Test Book 2', author='Author 2', published_date='2022-02-01')

    def test_get_book_list(self):
        url = reverse('book-list')  # Assuming you have named your URL patterns
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check if the correct number of objects is returned
        # Add more assertions based on your API response structure
