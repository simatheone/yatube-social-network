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
