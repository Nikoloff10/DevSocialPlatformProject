# Generated by Django 5.1.2 on 2024-11-14 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devsearchey', '0017_forumpost_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumpost',
            name='category',
            field=models.CharField(choices=[('dev_problems', 'Dev Problems and Discussions'), ('techy_nerds', 'Techy Nerds')], default='dev_problems', max_length=20),
        ),
    ]
