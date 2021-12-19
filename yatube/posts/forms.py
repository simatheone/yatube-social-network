from django.forms import ModelForm, Textarea
from django import forms

from .models import Comment, Post


WIDGET = {
    'text': Textarea(attrs={'cols': 40, 'row': 10}),
}
VALIDATION_ERROR = 'Поле текст обязательно должно быть заполнено!'


class PostForm(ModelForm):
    """
    Форма для создания/редактирования поста.
    """
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        labels = {
            'text': 'Текст нового поста'
        }
        widgets = WIDGET

    def clean_text(self):
        """
        Функция валидатор, которая проверяет, что текствое поле
        не является пустым.
        """
        data = self.cleaned_data['text']
        if not data:
            raise forms.ValidationError(VALIDATION_ERROR)
        return data


class CommentForm(ModelForm):
    """
    Форма создания комментария.
    """
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = WIDGET

    def clean_text(self):
        """
        Функция валидатор, которая проверяет, что текстовое поле
        формы не является пустым.
        """
        data = self.cleaned_data['text']
        if not data:
            raise forms.ValidationError(VALIDATION_ERROR)
        return data
