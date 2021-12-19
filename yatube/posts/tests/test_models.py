from django.test import TestCase

from posts.models import Group, Post, User
from posts.tests.constants import (
    AUTHORIZED_USER, GROUP_DESCRIPTION, GROUP_SLUG_1, GROUP_TITLE, POST_TEXT
)


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создание тестовой БД."""
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHORIZED_USER)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG_1,
            description=GROUP_DESCRIPTION
        )
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.user,
        )

    def test_post_model_have_correct_object_name(self):
        """
        Тест проверяет, что у модели Post корректно работает метод __str__.
        """
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))

    def test_group_model_have_correct_object_name(self):
        """
        Тест проверяет, что у модели Group правильно работает метод __str__.
        """
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_post_verbose_name(self):
        """
        Тест проверяет, что у модели Post поля
        с указанным verbose_name отображаются правильно.
        """
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата',
            'author': 'Автор'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_post_help_text(self):
        """
        Тест проверяет, что у модели Post поля
        с указанным help_text отображаются правильно.
        """
        post = PostModelTest.post
        field_help_text = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу'
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )
