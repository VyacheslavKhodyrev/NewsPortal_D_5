from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter
from .models import *
from django.forms import DateInput, DateTimeInput

class PostFilter(FilterSet):
    title = CharFilter(
        lookup_expr='iregex',
        label='Заголовок содержит'
    )

    autoDate = DateFilter(
        lookup_expr='date__gte',
        label='Дата позднее',
        widget=DateInput(
            format='%d.%m.%Y',
            attrs={'type': 'date'}
        )
    )

    postCategory = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории'
    )

    postAuthor = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все авторы'
    )
