import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UniVerse.settings')  # Adjust this line with your project's settings module

application = get_asgi_application()
