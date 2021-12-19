from http import HTTPStatus

from django.test import TestCase, Client


class StaticURLTests(TestCase):

    def setUp(self):
        """Создание гостя для последующего использования в тестах."""
        self.guest_client = Client()

    def test_urls_exists_at_desired_locations(self):
        """
        Тест проверяет, что страницы об авторе и технологии
        существуют и их статус код '200'.
        """
        testing_urls = ('/about/author/', '/about/tech/')
        for adress in testing_urls:
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)
