# Generated by Django 5.1.2 on 2024-11-11 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devsearchey', '0015_create_sneaky_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumpost',
            name='comment_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='forumpost',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]