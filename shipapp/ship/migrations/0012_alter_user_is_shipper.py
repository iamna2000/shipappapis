# Generated by Django 3.2.6 on 2021-12-29 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ship', '0011_user_is_shipper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_shipper',
            field=models.BooleanField(default=False),
        ),
    ]