from django import template
import string

register = template.Library()

CENSORED_WORDS = [
    'спикер',
    'список',
    'магнитная',
    'буря',
]


@register.filter()
def censor(text):
    if type(text) is not str:
        raise TypeError('Переменная может иметь только строковый тип')
    else:
        new_text = text.split()
        censored_text = []

        for word in new_text:
            nw = word.lower()
            if nw.translate(str.maketrans('', '', string.punctuation)) in CENSORED_WORDS:
                new_word = word[0] + '*' * (len(word[1:]))
                censored_text.append(new_word)
            else:
                censored_text.append(word)

    return ' '.join(censored_text)
