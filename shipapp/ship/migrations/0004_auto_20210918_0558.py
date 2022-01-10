# Generated by Django 3.2.6 on 2021-09-17 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ship', '0003_auto_20210917_0523'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tag',
            new_name='Place',
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.AddField(
            model_name='post',
            name='delivery_point',
            field=models.ManyToManyField(related_name='delivery_point', to='ship.Place'),
        ),
        migrations.AddField(
            model_name='post',
            name='receipt_point',
            field=models.ManyToManyField(related_name='receipt_point', to='ship.Place'),
        ),
        migrations.AlterField(
            model_name='post',
            name='good',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ship.good'),
        ),
    ]
