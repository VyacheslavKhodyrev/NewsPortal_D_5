from django import forms
from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'postAuthor',
            'postCategory',
            'title',
            'postText'
        ]

        labels = {
            'postAuthor': 'Автор',
            'postCategory': 'Категории',
            'title': 'Заголовок',
            'postText': 'Содержание',
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'postAuthor',
            'postCategory',
            'title',
            'postText'
        ]

        labels = {
            'postAuthor': 'Автор',
            'postCategory': 'Категории',
            'title': 'Заголовок',
            'postText': 'Содержание',
        }










