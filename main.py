
from pathlib import Path
from dotenv import load_dotenv
import os

from account import account

load_dotenv()  # loads the configs from .env

BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = 'https://api.vultr.com/v2/'
SECRET_KEY = str(os.getenv('API_KEY'))

print(account(BASE_URL, SECRET_KEY))

