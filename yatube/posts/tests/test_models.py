from django.test import TestCase
from django.db.utils import IntegrityError

from posts.models import Comment, Follow, Group, Post, User
from posts.tests.constants import (
    AUTHORIZED_USER, GROUP_DESCRIPTION, GROUP_SLUG_1,
    GROUP_TITLE, HELP_TEXT_TEXT_COMMENNT, MAX_TEXT_RENDER,
    POST_AUTHOR, POST_TEXT, STR_FOR_FOLLOW, TEST_AUTHOR_MODEL,
    TEST_COMMENT_TEXT, TEST_CREATE_COMMENT_DATA, TEST_DATA, TEST_FIELD_TEXT,
    TEST_HELP_TEXT, TEST_HELP_TEXT_GROUP, TEST_IMAGE_VERBOSE, TEST_TEXT,
    VERBOSE_NAME_CREATED_COMMENT, VERBOSE_NAME_TEXT_COMMENT
)


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создание тестовой БД."""
        super().setUpClass()
        cls.user = User.objects.create(username=AUTHORIZED_USER)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG_1,
            description=GROUP_DESCRIPTION
        )
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.user,
        )

    def test_post_model_has_correct_object_name(self):
        """
        Тест проверяет, что у модели Post корректно работает метод __str__.
        """
        post = __class__.post
        expected_object_name = post.text[:MAX_TEXT_RENDER]
        self.assertEqual(expected_object_name, str(post))

    def test_group_model_has_correct_object_name(self):
        """
        Тест проверяет, что у модели Group правильно работает метод __str__.
        """
        group = __class__.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_post_verbose_name(self):
        """
        Тест проверяет, что у модели Post поля
        с указанным verbose_name отображаются правильно.
        """
        post = __class__.post
        field_verboses = {
            'text': TEST_TEXT,
            'pub_date': TEST_DATA,
            'author': TEST_AUTHOR_MODEL,
            'image': TEST_IMAGE_VERBOSE
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
        post = __class__.post
        field_help_text = {
            'text': TEST_HELP_TEXT,
            'group': TEST_HELP_TEXT_GROUP
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создание тестовой БД."""
        super().setUpClass()
        cls.user = User.objects.create(username=AUTHORIZED_USER)
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text=TEST_COMMENT_TEXT,
            created=TEST_CREATE_COMMENT_DATA
        )

    def test_comment_model_has_correct_obj_name(self):
        """
        Тест проверяет, что у модели Comment корректно работает метод __str__.
        """
        comment = __class__.comment
        expected_value = comment.text[:MAX_TEXT_RENDER]
        self.assertEqual(expected_value, str(comment))

    def test_comment_verbose_name(self):
        """
        Тест проверяет, что у модели Comment поля
        с указанным verbose_name отображаются правильно.
        """
        comment = __class__.comment
        field_verboses = {
            'text': VERBOSE_NAME_TEXT_COMMENT,
            'created': VERBOSE_NAME_CREATED_COMMENT
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).verbose_name, expected_value
                )

    def test_comment_help_text(self):
        """
        Тест проверяет, что у модели Comment поля
        с указанным help_text отображаются правильно.
        """
        comment = __class__.comment
        field_help_text = {
            'text': HELP_TEXT_TEXT_COMMENNT,
        }
        self.assertEqual(
            comment._meta.get_field(TEST_FIELD_TEXT).help_text,
            field_help_text[TEST_FIELD_TEXT]
        )


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создание тестовой БД."""
        super().setUpClass()
        cls.user = User.objects.create(username=AUTHORIZED_USER)
        cls.author = User.objects.create(username=POST_AUTHOR)
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.author
        )
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.author
        )

    def test_follow_model_has_correct_obj_name(self):
        """
        Тест проверяет, что у модели Follow корректно работает метод __str__.
        """
        follow = __class__.follow
        expected_value = (f'{self.user.username} '
                          f'{STR_FOR_FOLLOW} {self.author.username}'
                          )
        self.assertEqual(expected_value, str(follow))

    def test_user_cant_follow_itself(self):
        """
        Тест проверяет, что на уровне модели юзер не может быть
        подписан сам на себя.
        """
        with self.assertRaises(IntegrityError):
            Follow.objects.create(
                user=self.user,
                author=self.user
            )

    def test_user_cant_follow_same_author_more_then_once(self):
        """
        Тест проверяет, что на уровне модели юзер не может быть
        подписан на одного автора более одного раза.
        """
        with self.assertRaises(IntegrityError):
            Follow.objects.create(
                user=self.user,
                author=self.author
            )
