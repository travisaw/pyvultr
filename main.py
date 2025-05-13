
from pathlib import Path
from dotenv import load_dotenv
import os

from api import Api
from menu import Menu

load_dotenv()  # loads the configs from .env

BASE_DIR = Path(__file__).resolve().parent.parent

api = Api(str(os.getenv('API_KEY')))
menu = Menu(api)
menu.main_menu()

# account(BASE_URL, SECRET_KEY)

