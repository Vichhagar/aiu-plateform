from django.test import TestCase
from django.shortcuts import reverse

class HomePageTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse("activity:home"))
        print(response)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, "activity/home.html")
