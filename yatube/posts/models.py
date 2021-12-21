from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import CheckConstraint, F, UniqueConstraint, Q
from django.db.models.deletion import CASCADE

User = get_user_model()


class Group(models.Model):
    """
    Модель группы для сохранения в базе данных.
    """
    title = models.CharField('Название группы', max_length=200)
    slug = models.SlugField('Тема группы', unique=True)
    description = models.TextField('Описание группы')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        """
        Функция возвращает название группы.
        """
        return self.title


class Post(models.Model):
    """
    Модель поста для сохранения в базе данных.
    """
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField('Дата', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        help_text='Выберите группу'
    )
    image = models.ImageField(
        'Картинка поста',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        """
        Функция возвращает текст поста, урезанного до 15 символов.
        """
        return self.text[:15]


class Comment(models.Model):
    """
    Модель комментариев к постам для сохранения в базе данных.
    """
    post = models.ForeignKey(
        Post,
        on_delete=CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        'Текст комментария к посту',
        help_text='Введите текст комментария'
    )
    created = models.DateTimeField(
        'Дата создания комментария',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """
        Функция возвращает текст комментария.
        """
        return self.text[:15]


class Follow(models.Model):
    """
    Модель подписки на авторов для сохранения в базе данных.
    user - ссылка на объект пользователя, который подписывается.
    author - ссылка на объект пользователя, на которого подписываются.
    """
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'], name='unique_follower'
            ),
            CheckConstraint(check=~Q(user=F('author')),
                            name='user_cant_follow_himself'),
        ]

    def __str__(self):
        return f'{self.user.username} подписался на {self.author.username}'
