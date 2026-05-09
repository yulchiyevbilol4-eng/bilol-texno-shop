import os
from django.core.wsgi import get_wsgi_application

# Papka nomi 'core' bo'lgani uchun 'core.settings' deb yoziladi
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

# Render/Vercel loyihani topishi uchun:
app = application