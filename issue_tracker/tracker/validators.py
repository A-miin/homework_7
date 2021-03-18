from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

@deconstructible
class MinLengthValidator(BaseValidator):
    message = 'Должно быть минимум %(limit_value)d сивволов!'
    code = 'too_short'

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        return len(x)

forbidden_symbols=['@','#','_', '/']
forbidden_words=['vasya', 'pupkin', 'author', 'title', 'заголовок']


def validate_string(value):
    for symbol in value:
        if symbol in forbidden_symbols:
            raise ValidationError(
                _(f'{value} не должно содержать символы {forbidden_symbols}')
            )


def validate_words(value):
    for word in value.split(' '):
        if word.lower() in forbidden_words:
            raise ValidationError(
                _('%(value)s содержит ненормативную лексику'),
                params={'value': value}
            )


def validate_words_count(value):
    print(f'value={value}')
    if len(value)!=0:
        if len(value.split(' '))<2:
            raise ValidationError(
                _('Если уж писать то Не менее двух слов!'),
            )


