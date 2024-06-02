from django.test import Client, TestCase


class Test(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_chat(self):
        response = self.client.get("/chat")

        self.assertEqual(response.status_code, 200)
