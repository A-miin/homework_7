# Generated by Django 3.1.7 on 2021-03-15 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_auto_20210315_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='type',
            field=models.ManyToManyField(blank=True, related_name='issues', to='tracker.Type', verbose_name='Тип'),
        ),
    ]
