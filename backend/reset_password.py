import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Get or create testuser
user, created = User.objects.get_or_create(username='testuser')
user.set_password('TestPass123')
user.email = 'test@example.com'
user.save()

print(f"User: {user.username}")
print(f"Email: {user.email}")
print(f"Password set to: TestPass123")
print(f"User ID: {user.id}")

# Test authentication
from django.contrib.auth import authenticate
auth_user = authenticate(username='testuser', password='TestPass123')
if auth_user:
    print("✓ Authentication SUCCESSFUL")
else:
    print("✗ Authentication FAILED")

# Get token
from rest_framework.authtoken.models import Token
token, created = Token.objects.get_or_create(user=user)
print(f"Token: {token.key}")
