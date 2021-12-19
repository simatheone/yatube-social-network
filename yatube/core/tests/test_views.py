from django.test import Client, TestCase


class CoreTest(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_unexisting_page_returns_custom_404_template(self):
        url = '/unexisting-page/'
        response = self.guest_client.get(url)
        self.assertTemplateUsed(response, 'core/404.html')
