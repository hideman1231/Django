# Generated by Django 3.1.5 on 2021-04-06 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myavio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, default='D:\\Desktop\\testick\\avio\\images.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='photo_url',
            field=models.URLField(blank=True, default='D:\\Desktop\\testick\\avio\\images.png'),
        ),
    ]
