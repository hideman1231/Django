# Generated by Django 3.1.5 on 2021-02-05 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchase',
            options={'ordering': ['-purchase_time']},
        ),
        migrations.AlterModelOptions(
            name='purchasereturn',
            options={'ordering': ['-return_time']},
        ),
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
