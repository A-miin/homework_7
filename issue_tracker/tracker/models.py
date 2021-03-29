from django.db import models
from django.core.exceptions import ValidationError
from .validators import MinLengthValidator, validate_string, validate_words, validate_words_count


# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='Тип')

    class Meta:
        verbose_name="Тип"
        verbose_name_plural="Типы"

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='Статус')

    class Meta:
        verbose_name="Статус"
        verbose_name_plural="Статусы"

    def __str__(self):
        return self.name

class Issue(models.Model):
    summary = models.CharField(max_length=120, null=False, blank=False, verbose_name='Краткое описание',validators=[validate_string, validate_words, MinLengthValidator(3)])
    description = models.TextField(max_length=1024,null=True, blank=True, verbose_name='Полное описание', validators=[validate_words_count, validate_words])
    status = models.ForeignKey('tracker.Status', on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ManyToManyField('tracker.Type', related_name="issues", verbose_name='Тип', blank=True)
    project = models.ForeignKey('tracker.Project', on_delete=models.CASCADE, related_name='issues', verbose_name="Проект")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name='Задача'
        verbose_name_plural='Задачи'


    def __str__(self):
        return f'{self.id}. {self.summary}: {self.type}'


class Project(models.Model):
    begin_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата конца", null=True, blank=False)
    name = models.CharField(max_length=120, verbose_name="Название")
    description = models.TextField(max_length=3072, verbose_name="Описание")

    class Meta:
        verbose_name="Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return f'{self.name}: {self.begin_date}/{self.end_date}'

