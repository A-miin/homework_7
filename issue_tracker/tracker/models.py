from django.db import models

# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='Тип')

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='Статус')

    def __str__(self):
        return self.name


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
