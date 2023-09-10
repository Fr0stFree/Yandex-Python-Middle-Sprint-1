from pathlib import Path

import environ
from dotenv import find_dotenv
from split_settings.tools import include

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

env.read_env(env_file=find_dotenv('.env'))

SECRET_KEY = env.str('DJANGO_SECRET_KEY')

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
INTERNAL_IPS = env.list('INTERNAL_IPS')

include(
    'components/database.py',
    'components/apps.py',
    'components/middleware.py',
    'components/validation.py',
    'components/rendering.py',
    'components/timezone.py',
    'components/locale.py',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

EMPTY_VALUE_DISPLAY = '-пусто-'
