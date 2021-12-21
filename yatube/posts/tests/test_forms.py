from http import HTTPStatus
from shutil import rmtree
from tempfile import mkdtemp

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, override_settings, TestCase
from django.urls import reverse

from posts.models import Comment, Group, Post, User
from posts.tests.constants import (
    FORM_ERROR, GROUP_DESCRIPTION, GROUP_TITLE, GROUP_SLUG_2, FORM_ERROR,
    POST_AUTHOR, POST_CREATE_URL, POST_TEXT, POST_TEXT_EDITED_1,
    POST_TEXT_EDITED_2, POST_TEXT_FORM_DATA_1, POST_TEXT_FORM_DATA_2,
    PROFILE_URL, SMALL_IMAGE
)

TEMP_MEDIA_ROOT = mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """Создание тестовой БД."""
        super().setUpClass()
        cls.author = User.objects.create(username=POST_AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG_2,
            description=GROUP_DESCRIPTION
        )
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.author
        )
        cls.POST_DETAIL_URL = (reverse('posts:post_detail',
                                       args=(cls.post.id,)),
                               'posts/post_detail.html'
                               )
        cls.POST_EDIT_URL = (reverse('posts:post_edit',
                                     args=(cls.post.id,)),
                             'posts/create_post.html'
                             )

    def setUp(self):
        """Создание клиентов для последующего использования в тестах."""
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)
        self.upload = SimpleUploadedFile(
            name='small_image.gif',
            content=SMALL_IMAGE,
            content_type='image/gif'
        )

    def tearDown(self):
        rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_form_creates_post_without_group(self):
        """
        Тест проверяет, что при отправке валидной формы без группы
        в базе данных создается пост.
        """
        posts_count = Post.objects.count()
        form_data = {
            'text': POST_TEXT_FORM_DATA_1,
            'image': self.upload
        }
        response = self.authorized_author.post(
            POST_CREATE_URL[1],
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            PROFILE_URL[1]
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=POST_TEXT_FORM_DATA_1,
                image=f'posts/{self.upload.name}'
            ).exists()
        )

    def test_form_creates_post_with_group(self):
        """
        Тест проверяет, что при отправке валидной формы с группой
        в базе данных создается пост.
        """
        posts_count = Post.objects.count()
        form_data = {
            'text': POST_TEXT_FORM_DATA_2,
            'group': self.group.pk,
            'image': self.upload
        }
        response = self.authorized_author.post(
            POST_CREATE_URL[1],
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            PROFILE_URL[1]
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=POST_TEXT_FORM_DATA_2,
                group=self.group.pk,
                image=f'posts/{self.upload.name}'
            ).exists()
        )

    def test_cant_create_form_without_text(self):
        """
        Тест проверяет, что при отправке невалидной формы
        поста появляется сообщение об ошибке.
        """
        posts_count = Post.objects.count()
        form_data = {
            'text': ''
        }
        response = self.authorized_author.post(
            POST_CREATE_URL[1],
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertFormError(
            response,
            'form',
            'text',
            FORM_ERROR
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_form_without_group(self):
        """
        Тест проверяет, что при отправке валидной формы без группы
        со страницы редактирования поста происходит изменение в БД.
        """
        form_data = {
            'text': 'Измененный текст поста'
        }
        response = self.authorized_author.post(
            self.POST_EDIT_URL[0],
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            self.POST_DETAIL_URL[0]
        )
        self.assertTrue(
            Post.objects.filter(text=POST_TEXT_EDITED_1).exists()
        )

    def test_post_edit_form_with_group(self):
        """
        Тест проверяет, что при отправке валидной формы с группой
        со страницы редактирования поста происходит изменение в БД.
        """
        form_data = {
            'text': POST_TEXT_EDITED_2,
            'group': self.group.pk
        }
        response = self.authorized_author.post(
            self.POST_EDIT_URL[0],
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            self.POST_DETAIL_URL[0]
        )
        self.assertTrue(
            Post.objects.filter(
                text=POST_TEXT_EDITED_2,
                group=self.group.pk
            ).exists()
        )

    def test_cant_post_comment_form_without_text(self):
        """
        Тест проверяет, что при отправке невалидной формы
        комментария появляется сообщение об ошибке.
        """
        comments_count = Comment.objects.count()
        comment_data = {
            'text': ''
        }
        response = self.authorized_author.post(
            self.POST_DETAIL_URL[0],
            data=comment_data,
            follow=True
        )
        self.assertEqual(Comment.objects.count(), comments_count)
        self.assertFormError(
            response,
            'form',
            'text',
            FORM_ERROR
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
