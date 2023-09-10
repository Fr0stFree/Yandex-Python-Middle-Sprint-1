import environ
from dotenv import find_dotenv

env = environ.Env()
env.read_env(env_file=find_dotenv('.env'))
