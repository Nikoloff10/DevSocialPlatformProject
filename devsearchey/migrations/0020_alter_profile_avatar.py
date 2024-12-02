# Generated by Django 5.1.2 on 2024-11-18 14:06

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devsearchey', '0019_jobpost_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=cloudinary.models.CloudinaryField(default='avatars/default.jpg', max_length=255, verbose_name='image'),
        ),
    ]
