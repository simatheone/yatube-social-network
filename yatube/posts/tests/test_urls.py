from http import HTTPStatus

from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Group, Post, User
from posts.tests.constants import (
    AUTHORIZED_USER, GROUP_DESCRIPTION, GROUP_TITLE, GROUP_LIST_URL,
    GROUP_SLUG_1, INDEX_URL, POST_AUTHOR, POST_CREATE_URL,
    POST_TEXT, PROFILE_URL, REDIRECT
)


class PostURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """Создание тестовой БД."""
        super().setUpClass()
        cls.author = User.objects.create(username=POST_AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG_1,
            description=GROUP_DESCRIPTION
        )
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.author,
            group=cls.group
        )
        cls.POST_DETAIL_URL = ('post_detail',
                               reverse('posts:post_detail',
                                       args=(cls.post.id,)),
                               'posts/post_detail.html'
                               )
        cls.POST_EDIT_URL = ('post_edit',
                             reverse('posts:post_edit',
                                     args=(cls.post.id,)),
                             'posts/create_post.html'
                             )
        cls.urls = {
            'index': INDEX_URL,
            'group_list': GROUP_LIST_URL,
            'profile': PROFILE_URL,
            'create': POST_CREATE_URL,
            'post_detail': cls.POST_DETAIL_URL,
            'post_edit': cls.POST_EDIT_URL
        }

    def setUp(self):
        """Создание клиентов для последующего использования в тестах."""
        self.guest_client = Client()
        self.authorized_client = Client()
        self.author_client = Client()
        self.user = User.objects.create_user(username=AUTHORIZED_USER)
        self.authorized_client.force_login(self.user)
        self.author_client.force_login(self.author)

    def tearDown(self):
        """
        Функиция, которая чистит кэш после каждого теста.
        """
        cache.clear()

    def test_urls_exists_at_desired_location_authorized(self):
        """
        Тест проверяет, что страницы существуют по заданным адреса.
        Для несуществующей страници проверка на статус Not found.
        """
        for url_name, params in self.urls.items():
            with self.subTest(url_name=url_name):
                response = self.author_client.get(params[1])
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_templates(self):
        """
        Тест проверяет, что страницы использую
        правильные шаблоны для рендеринга.
        """
        for url_name, params in self.urls.items():
            with self.subTest(url_name=url_name):
                response = self.author_client.get(params[1])
                self.assertTemplateUsed(response, params[2])

    def test_non_existent_page_not_found(self):
        """
        Тест проверяет, что статус несуществующей старнице 404.
        """
        url = '/unexisting_page/'
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_redirects_anonymous_on_login_page(self):
        """
        Тест проверяет, что незарегестированный пользователь,
        при попытке доступа к страницам create/, edit/
        перенаправляется на страницу авторизации.
        """
        urls_redirects = {
            self.urls['post_edit'][1]: REDIRECT + self.urls['post_edit'][1],
            self.urls['create'][1]: REDIRECT + self.urls['create'][1]
        }
        for url, redirect_page in urls_redirects.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, redirect_page)

    def test_urls_wrong_author_tries_edit_post(self):
        """
        Тест проверяет, что пользователь, не являющийся автором
        поста, при попытке редактирования поста, будет перенаправлен
        на страницу с подробной нформацией об этом посте.
        """
        response = self.authorized_client.get(
            self.urls['post_edit'][1],
            follow=True
        )
        self.assertRedirects(response, self.urls['post_detail'][1])
