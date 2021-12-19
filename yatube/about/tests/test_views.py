from django.test import TestCase, Client


class StaticURLTests(TestCase):

    def setUp(self):
        """Создание гостя для последующего использования в тестах."""
        self.guest_client = Client()

    def test_page_uses_correct_template(self):
        """
        Тест проверяет, что страницы об авторе и технологии
        используют правильные темплейты для рендеринга.
        """
        template_names = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/'
        }
        for template, adress in template_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)
