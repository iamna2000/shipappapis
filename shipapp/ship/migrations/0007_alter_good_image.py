# Generated by Django 3.2.6 on 2021-09-17 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ship', '0006_alter_good_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='image',
            field=models.ImageField(upload_to='goods/%Y/%m'),
        ),
    ]
