# Generated by Django 3.2.6 on 2021-12-29 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ship', '0015_lessonview'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LessonView',
            new_name='PostView',
        ),
    ]