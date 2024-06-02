import unittest

from django.test import Client


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_chat(self):
        response = self.client.get("/chat")

        self.assertEqual(response.status_code, 200)
