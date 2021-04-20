from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE,
                                verbose_name="Пользователь")
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars', verbose_name="Аватар")
    githubLink = models.URLField(null=True, blank=True, max_length=512, verbose_name="Ссылка на гитхаб")
    description = models.TextField(max_length=2048, null=True, blank=True, verbose_name="О себе")

    class Meta:
        verbose_name="Профиль"
        verbose_name_plural="Профили"
        permissions=[
            ('can_view_profiles','Can view profiles')
        ]

    def __str__(self):
        return f'{self.user.get_full_name()} profile'

