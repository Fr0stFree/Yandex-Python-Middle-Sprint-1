from pathlib import Path

from config.components import env

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = env.bool('DEBUG')
SECRET_KEY = env.str('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
INTERNAL_IPS = env.list('INTERNAL_IPS')
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
