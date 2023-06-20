import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))


load_dotenv(os.path.join(BASEDIR, '.env'))

EXAMPLE_API = os.getenv('EXAMPLE_API')

API = os.getenv('API')
