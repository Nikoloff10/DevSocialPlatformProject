from django.db import migrations
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def create_sneaky_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    password_hash = make_password('password')
    User.objects.update_or_create(username='Sneaky', defaults={
    
    'password': password_hash,  
    'is_staff': False,
    'is_superuser': False,
    'email': ''})
    

class Migration(migrations.Migration):

    dependencies = [
        
        ('devsearchey', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sneaky_user),
    ]