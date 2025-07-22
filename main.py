
from pathlib import Path
from dotenv import load_dotenv
import os
import importlib.util

def module_exists(module_name):
    return importlib.util.find_spec(module_name) is not None

if not module_exists('settings'):
    print("The 'settings' module is required but not found!! Please copy settings.py.template to settings.py.")
    exit(1)

from api.vultr import Vultr
from api.cloudflare import Cloudflare
from menu import Menu

load_dotenv()  # loads the configs from .env

BASE_DIR = Path(__file__).resolve().parent.parent # Set base directory

# Load APIs using keys from config file. Display main menu.
vultr_api = Vultr(str(os.getenv('VULTR_API_KEY')))
cloudflare_api = Cloudflare(str(os.getenv('CLOUDFLARE_EMAIL')), str(os.getenv('CLOUDFLARE_API_KEY')))
menu = Menu(vultr_api, cloudflare_api)
menu.main_menu()
