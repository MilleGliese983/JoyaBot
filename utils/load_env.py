from os.path import join, dirname
from os import environ
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), "../settings/.env"))

INSTANCE_URL = environ.get("INSTANCE_URL")
ACCESS_TOKEN = environ.get("ACCESS_TOKEN")