# Generated by Django 3.1.5 on 2021-01-21 12:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20210121_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='article creation'),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='article update'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name='article content'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=50, verbose_name='article name'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='comment creation'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='comment update'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='comment content'),
        ),
    ]
