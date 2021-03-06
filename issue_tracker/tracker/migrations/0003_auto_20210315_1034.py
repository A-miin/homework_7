# Generated by Django 3.1.7 on 2021-03-15 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20210311_0819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Статус', 'verbose_name_plural': 'Статусы'},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'verbose_name': 'Тип', 'verbose_name_plural': 'Типы'},
        ),
        migrations.CreateModel(
            name='IssueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_types', to='tracker.issue', verbose_name='Задача')),
                ('issue_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_issues', to='tracker.type', verbose_name='Тип')),
            ],
        ),
        migrations.AddField(
            model_name='type',
            name='issues',
            field=models.ManyToManyField(blank=True, related_name='types', through='tracker.IssueType', to='tracker.Issue'),
        ),
    ]
