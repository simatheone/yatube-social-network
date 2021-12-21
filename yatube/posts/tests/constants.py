from django.urls import reverse

# Константы используемые для создания тестовой БД и тестовых юзеров
AUTHORIZED_USER = 'Testuser'
COMMENT = 'Тестовый комментарий'
GROUP_DESCRIPTION = 'Тестовое описание группы'
GROUP_DESCRIPTION_1 = 'Тестовое описание группы 1'
GROUP_DESCRIPTION_2 = 'Тестовое описание группы 2'
GROUP_TITLE = 'Тестовое название группы'
GROUP_TITLE_1 = 'Тестовая группы 1'
GROUP_TITLE_2 = 'Тестовая группы 2'
GROUP_SLUG_1 = 'test-slug-1'
GROUP_SLUG_2 = 'test-slug-2'
POST_AUTHOR = 'TestAuthor'
POST_AUTHOR_2 = 'TestAuthor 2'
POST_TEXT = 'Тестовый текст поста'

# Константы для теста моделей
TEST_IMAGE_VERBOSE = 'Картинка поста'
TEST_DATA = 'Дата'
TEST_AUTHOR_MODEL = 'Автор'
MAX_TEXT_RENDER = 15
TEST_TEXT = 'Текст поста'
TEST_HELP_TEXT = 'Введите текст поста'
TEST_HELP_TEXT_GROUP = 'Выберите группу'
TEST_COMMENT_TEXT = 'Тестовый комментарий'
TEST_CREATE_COMMENT_DATA = '05.12.1995'
VERBOSE_NAME_TEXT_COMMENT = 'Текст комментария к посту'
HELP_TEXT_TEXT_COMMENNT = 'Введите текст комментария'
VERBOSE_NAME_CREATED_COMMENT = 'Дата создания комментария'
TEST_FIELD_TEXT = 'text'
STR_FOR_FOLLOW = 'подписался на'

# Константы для проврки контекста в test_views.py
GROUP_LIST_CONTEXT_TITLE = 'Записи сообщества'
INDEX_CONTEXT_TITLE = 'Последние обновления на сайте'

# Константы для test_forms
POST_TEXT_FORM_DATA_1 = 'Тестовый текст созданного поста 2'
POST_TEXT_FORM_DATA_2 = 'Тестовый текст созданного поста 3'
POST_TEXT_EDITED_1 = 'Измененный текст поста'
POST_TEXT_EDITED_2 = 'Измененный текст поста 2'
FORM_ERROR = 'Обязательное поле.'

# Константы URL используемые в test_urls, test_views, test_forms
# Каждая константа хранит в себе кортеж данных о странице
# вида: (page name, reversed page url, page template)
INDEX_URL = ('index', reverse('posts:index'), 'posts/index.html')
GROUP_LIST_URL = ('group_list',
                  reverse('posts:group_list', args=(GROUP_SLUG_1,)),
                  'posts/group_list.html'
                  )
POST_CREATE_URL = ('post_create', reverse('posts:post_create'),
                   'posts/create_post.html'
                   )
PROFILE_URL = ('profile',
               reverse('posts:profile', args=(POST_AUTHOR,)),
               'posts/profile.html'
               )

FOLLOW_PAGE = (reverse('posts:follow_index'), 'posts/follow.html')

# Константа для проверки редиректа, используется в test_urls
REDIRECT = '/auth/login/?next='

# Вторая страница пагинатора
PAGE_2 = '?page=2'

# Константа картинки, используемая в тестах
SMALL_IMAGE = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
