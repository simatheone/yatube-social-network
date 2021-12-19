from shutil import rmtree
from tempfile import mkdtemp
from http import HTTPStatus

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, override_settings, TestCase
from django.urls import reverse
from django import forms

from posts.models import Comment, Follow, Group, Post, User
from yatube.settings import POSTS_ON_PAGE
from posts.tests.constants import (
    AUTHORIZED_USER, COMMENT, FOLLOW_PAGE, GROUP_DESCRIPTION,
    GROUP_DESCRIPTION_1, GROUP_DESCRIPTION_2, GROUP_LIST_CONTEXT_TITLE,
    GROUP_TITLE, GROUP_TITLE_1, GROUP_TITLE_2, GROUP_LIST_URL, GROUP_SLUG_1,
    GROUP_SLUG_2, INDEX_CONTEXT_TITLE, INDEX_URL, PAGE_2, POST_AUTHOR,
    POST_AUTHOR_2, POST_CREATE_URL, POST_TEXT, PROFILE_URL, REDIRECT
)


TEMP_MEDIA_ROOT = mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """Создание тестовой БД."""
        super().setUpClass()
        cls.small_image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.upload = SimpleUploadedFile(
            name='small_image.gif',
            content=cls.small_image,
            content_type='image/gif'
        )
        cls.image = cls.upload
        cls.group = Group.objects.create(title=GROUP_TITLE_1,
                                         slug=GROUP_SLUG_1,
                                         description=GROUP_DESCRIPTION_1)
        Group.objects.create(title=GROUP_TITLE_2,
                             slug=GROUP_SLUG_2,
                             description=GROUP_DESCRIPTION_2)
        cls.author = User.objects.create(username=POST_AUTHOR)
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.author,
            group=cls.group,
            image=cls.image
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
        cls.ADD_COMMENT_URL = reverse('posts:add_comment',
                                      args=(cls.post.id,))
        cls.urls = {
            'index': INDEX_URL,
            'group_list': GROUP_LIST_URL,
            'profile': PROFILE_URL,
            'create': POST_CREATE_URL,
            'post_detail': cls.POST_DETAIL_URL,
            'post_edit': cls.POST_EDIT_URL,
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        """Создание клиентов для последующего использования в тестах."""
        self.user = User.objects.create_user(username=AUTHORIZED_USER)
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_author = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_author.force_login(self.author)

    def tearDown(self):
        """
        Функиция, которая чистит кэш после каждого теста.
        """
        cache.clear()

    def test_pages_use_correct_template_authorized(self):
        """
        Тест проверяет, что view-функции используют
        правильные html шаблоны.
        """
        for url_name, params in self.urls.items():
            with self.subTest(url_name=url_name):
                response = self.authorized_author.get(params[1])
                self.assertTemplateUsed(response, params[2])

    def test_correct_context_on_pages(self):
        """
        Тест проверяет, что на страницах index, profile, group_list
        используется правильный context.
        """
        responses = {
            INDEX_URL[0]: self.guest_client.get(INDEX_URL[1]),
            GROUP_LIST_URL[0]: self.authorized_client.get(GROUP_LIST_URL[1]),
            PROFILE_URL[0]: self.guest_client.get(PROFILE_URL[1])
        }
        titles = {
            'index': INDEX_CONTEXT_TITLE,
            'group_list': GROUP_LIST_CONTEXT_TITLE,
            'profile': None
        }
        for page, resp in responses.items():
            with self.subTest(page=page):
                first_object = resp.context['page_obj'][0]
                first_object_title = resp.context.get('title')
                self.assertEqual(first_object_title, titles[page])
                self.assertEqual(first_object.text, POST_TEXT)
                self.assertEqual(first_object.author.username, POST_AUTHOR)
                self.assertEqual(first_object.image,
                                 f'posts/{self.image.name}'
                                 )
                self.assertEqual(first_object.group.title,
                                 GROUP_TITLE_1)
                self.assertNotEqual(first_object.group.title,
                                    GROUP_TITLE_2)

    def test_correct_context_on_post_detail_page(self):
        """
        Тест проверяет, что для страницы posts/post_id/
        используется правильный context.
        """
        response = self.guest_client.get(self.urls['post_detail'][1])
        page_context = response.context.get('post')
        post_counter = response.context.get('count_posts')
        self.assertEqual(page_context.text, POST_TEXT)
        self.assertEqual(page_context.author.username, POST_AUTHOR)
        self.assertEqual(page_context.group.title,
                         GROUP_TITLE_1)
        self.assertEqual(page_context.group.slug, GROUP_SLUG_1)
        self.assertEqual(page_context.group.description,
                         GROUP_DESCRIPTION_1)
        self.assertEqual(page_context.image, f'posts/{self.image.name}')
        self.assertEqual(post_counter, self.post.author.posts.count())

    def test_correct_context_on_post_create_page(self):
        """
        Тест проверяет, что для страницы create/
        используется правильный context.
        """
        response = self.authorized_client.get(self.urls['create'][1])
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField
        }
        for value, expected_value in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected_value)

    def test_correct_context_on_post_edit_page(self):
        """
        Тест проверяет, что для страницы edit/
        используется правильный context.
        """
        response = self.authorized_author.get(self.urls['post_edit'][1])
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField
        }
        for value, expected_value in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected_value)

    def test_correct_context_on_post_edit_page_with_initial_value(self):
        """
        Тест проверяет, что в на странице edit/
        поле 'text' формы заполнено текстом для редактирования.
        """
        response = self.authorized_author.get(self.urls['post_edit'][1])
        initial_text = response.context['form'].initial['text']
        self.assertEqual(initial_text, POST_TEXT)

    def test_index_page_caches_correctly(self):
        """
        Тест проверяет правильность работы кэш.
        """
        response_first = self.guest_client.get(self.urls['index'][1])
        content_of_page_first = response_first.content
        Post.objects.all().delete()
        response_second = self.guest_client.get(self.urls['index'][1])
        self.assertEqual(response_second.content, content_of_page_first)

    def test_unauthorized_user_cant_write_comments(self):
        """
        Тест проверяет, что не авторизованный пользователь не
        может оставлять комментарии и перенаправляется на страницу авторизации.
        """
        comment_data = {
            'text': COMMENT,
        }
        response = self.guest_client.post(
            self.ADD_COMMENT_URL,
            data=comment_data,
            follow=True
        )
        self.assertRedirects(
            response,
            REDIRECT + self.ADD_COMMENT_URL
        )

    def test_authorized_user_can_write_comments(self):
        """
        Тест проверяет, что авторизованный пользователь может
        оставить комментарии и перенаправляется на страницу поста.
        """
        comment_data = {
            'text': COMMENT,
        }
        response = self.authorized_client.post(
            self.ADD_COMMENT_URL,
            data=comment_data,
            follow=True
        )
        self.assertRedirects(
            response,
            self.POST_DETAIL_URL[1]
        )
        self.assertTrue(
            Comment.objects.filter(text=COMMENT).exists()
        )
        self.assertEqual(
            Comment.objects.get(text=COMMENT).post_id,
            self.post.id
        )


class PaginatorViewsTest(TestCase):

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
        cls.post = Post.objects.bulk_create([
            Post(text=POST_TEXT + ' ' + str(i),
                 author=cls.author,
                 group=cls.group)
            for i in range(1, 13)]
        )
        cls.urls = (INDEX_URL, GROUP_LIST_URL, PROFILE_URL)

    def setUp(self):
        """Создание клиентов для последующего использования в тестах."""
        self.guest_client = Client()
        self.user = User.objects.create_user(username=AUTHORIZED_USER)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def tearDown(self):
        """
        Функиция, которая чистит кэш после каждого теста.
        """
        cache.clear()

    def test_paginator_for_index_page(self):
        """
        Тест проверяет, что пагинатор работает верно и
        на первых страницах index, group_list, profile выводится 10 постов.
        """
        for url_name, url, template in self.urls:
            with self.subTest(url_name=url_name):
                response_page_1 = self.guest_client.get(url)
                response_page_2 = self.guest_client.get(url + PAGE_2)
                self.assertEqual(
                    len(response_page_1.context['page_obj']), POSTS_ON_PAGE
                )
                self.assertEqual(len(response_page_2.context['page_obj']),
                                 len(self.post) - POSTS_ON_PAGE)


class FollowTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """Создание тестовой БД."""
        super().setUpClass()
        cls.author = User.objects.create(username=POST_AUTHOR)
        cls.author_2 = User.objects.create(username=POST_AUTHOR_2)
        cls.user = User.objects.create(username=AUTHORIZED_USER)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG_1,
            description=GROUP_DESCRIPTION
        )
        cls.posts_1 = Post.objects.bulk_create([
            Post(text=POST_TEXT + ' ' + str(i),
                 author=cls.author,
                 group=cls.group)
            for i in range(1, 12)]
        )
        cls.posts_2 = Post.objects.bulk_create([
            Post(text=POST_TEXT + ' ' + str(i),
                 author=cls.author_2,
                 group=cls.group)
            for i in range(1, 6)]
        )
        Follow.objects.create(user=cls.user, author=cls.author)
        cls.follow_url = reverse('posts:profile_follow',
                                 args=(POST_AUTHOR,))
        cls.unfollow_url = reverse('posts:profile_unfollow',
                                   args=(POST_AUTHOR,))

    def setUp(self):
        """Создание клиентов для последующего использования в тестах."""
        self.guest_client = Client()
        self.auth_user = Client()
        self.auth_author = Client()
        self.auth_author_2 = Client()
        self.auth_user.force_login(self.user)
        self.auth_author.force_login(self.author)
        self.auth_author_2.force_login(self.author_2)

    def test_posts_of_following_author_appers_on_followers_page(self):
        """
        Тест проверяет, что записи пользователя появляются в ленте
        тех юзеров, которые на него подписаны и не появляются в ленте
        тех, кто на него не подписан.
        """
        response_for_follower_page_1 = self.auth_user.get(FOLLOW_PAGE[0])
        response_for_follower_page_2 = self.auth_user.get(
            FOLLOW_PAGE[0] + PAGE_2
        )
        response_for_non_follower = self.auth_author.get(FOLLOW_PAGE[0])
        posts_from_db = []
        posts_from_context = []

        for post in Post.objects.filter(author=self.author)[:POSTS_ON_PAGE]:
            posts_from_db.append(post.text)

        for i in range(POSTS_ON_PAGE):
            post = response_for_follower_page_1.context['page_obj'][i]
            posts_from_context.append(post.text)

        non_follower_posts = response_for_non_follower.context['page_obj']

        self.assertEqual(posts_from_db, posts_from_context)
        self.assertNotEqual(len(non_follower_posts), POSTS_ON_PAGE)
        self.assertEqual(
            len(response_for_follower_page_1.context['page_obj']),
            POSTS_ON_PAGE
        )
        self.assertEqual(
            len(response_for_follower_page_2.context['page_obj']),
            len(self.posts_1) - POSTS_ON_PAGE
        )

    def test_follow_page_uses_correct_template(self):
        """
        Тест проверяет, что страница follow/ использует корректный темплэйт.
        """
        response = self.auth_user.get(FOLLOW_PAGE[0])
        self.assertTemplateUsed(response, FOLLOW_PAGE[1])

    def test_auth_unfollowing_user_can_follow_authors(self):
        """
        Тест проверяет, что авторизованный пользователь может
        подписываться на других пользователей.
        """
        follow_count = Follow.objects.filter(author=self.author).count()
        response_to_follow = self.auth_author_2.get(self.follow_url)
        self.assertEqual(response_to_follow.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            Follow.objects.filter(author=self.author).count(),
            follow_count + 1
        )

    def test_auth_following_user_can_unfollow_authors(self):
        """
        Тест проверяет, что авторизованный пользователь может
        отписываться от авторов.
        """
        unfollow_count = Follow.objects.filter(author=self.author).count()
        response_to_unfollow = self.auth_user.get(self.unfollow_url)
        self.assertEqual(response_to_unfollow.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            Follow.objects.filter(author=self.author).count(),
            unfollow_count - 1
        )

    def test_auth_user_cant_follow_one_author_twice(self):
        """
        Тест проверяет, что нельзя дважды подписаться на одного и
        того же автора.
        """
        follow_count = Follow.objects.filter(author=self.author).count()
        response_to_follow = self.auth_user.get(self.follow_url)
        self.assertEqual(response_to_follow.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            Follow.objects.filter(author=self.author).count(),
            follow_count
        )

    def test_author_cant_follow_himself(self):
        """
        Тест проверяет, что автор не может подписаться сам на себя.
        """
        follow_count = Follow.objects.filter(author=self.author).count()
        response_to_follow = self.auth_author.get(self.follow_url)
        self.assertEqual(response_to_follow.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            Follow.objects.filter(author=self.author).count(),
            follow_count
        )

    def test_guest_client_cant_follow_authors(self):
        """
        Тест проверяет, что незарегестрированный пользователь
        не может подписываться на авторов. При попытки захардкодить
        страницу, пользователь будет перенаправлен на страницу
        авторизации.
        """
        response_follow = self.guest_client.get(self.follow_url)
        self.assertEqual(response_follow.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response_follow, REDIRECT + self.follow_url)
