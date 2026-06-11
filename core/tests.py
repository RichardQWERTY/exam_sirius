from django.test import TestCase
from django.urls import reverse


class SmokeTests(TestCase):
    def test_ping_returns_200(self):
        response = self.client.get("/ping/")
        self.assertEqual(response.status_code, 200)

    def test_index_returns_200(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_create_page_returns_200(self):
        response = self.client.get(reverse("create"))
        self.assertEqual(response.status_code, 200)

    def test_update_missing_returns_404(self):
        response = self.client.get(reverse("update", args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_delete_missing_returns_404(self):
        response = self.client.get(reverse("delete", args=[99999]))
        self.assertEqual(response.status_code, 404)
