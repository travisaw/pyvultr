
from pathlib import Path
from dotenv import load_dotenv
import os

from api.vultr import Vultr
from api.cloudflare import Cloudflare
from menu import Menu

load_dotenv()  # loads the configs from .env

BASE_DIR = Path(__file__).resolve().parent.parent

vultr_api = Vultr(str(os.getenv('VULTR_API_KEY')))
cloudflare_api = Cloudflare(str(os.getenv('CLOUDFLARE_EMAIL')), str(os.getenv('CLOUDFLARE_API_KEY')))
menu = Menu(vultr_api, cloudflare_api)
menu.main_menu()

# account(BASE_URL, SECRET_KEY)

