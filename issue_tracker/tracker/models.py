from django.db import models

# Create your models here.
TYPE_CHOICES=[('task','задача'),('bug','ошибка'),('enhancement','улучшение')]
STATUS_CHOICES=[('new','новый'),('in progress','в процессе'),('done','выполнено')]
class Type(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='Тип',choices=TYPE_CHOICES, default='task')

class Status(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='Статус',choices=STATUS_CHOICES, default='new')

class Issue(models.Model):
    summary = models.CharField(max_length=120, null=False, blank=False, verbose_name='Краткое описание')
    description = models.TextField(max_length=1024, verbose_name='Полное описание')
    status = models.ForeignKey('tracker.Status', on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ForeignKey('tracker.Type', on_delete=models.PROTECT, verbose_name='Тип')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name='Задача'
        verbose_name_plural='Задачи'

    def __str__(self):
        return f'{self.id}. {self.summary}: {self.type}'
