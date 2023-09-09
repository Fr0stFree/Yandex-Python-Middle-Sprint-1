from dotenv import find_dotenv
from environ import Env

env = Env()
env.read_env(env_file=find_dotenv('.env'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': env.int('POSTGRES_PORT'),
        'OPTIONS': {
            'options': f'-c search_path={env.str("POSTGRES_SEARCH_PATHS")}',
        },
    },
}
