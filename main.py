
from pathlib import Path
from dotenv import load_dotenv
import os
import importlib.util
from util import yellow_text, red_text

def module_exists(module_name):
    return importlib.util.find_spec(module_name) is not None

if not module_exists('settings'):
    print("The 'settings' module is required but not found!! Please copy settings.py.template to settings.py.")
    exit(1)

import settings

load_dotenv()  # loads the configs from .env

# Validate required .env variables
required_env_vars = ['VULTR_API_KEY', 'CLOUDFLARE_EMAIL', 'CLOUDFLARE_API_KEY']
missing_env = [v for v in required_env_vars if not os.getenv(v)]
if missing_env:
    print(f"Missing required .env variables: {', '.join(missing_env)}")
    print("Please copy .env.template to .env and fill in your values.")
    exit(1)

# Set defaults if parameter doesn't exist
if not hasattr(settings, 'PRINT_TIMESTAMP'):
    print(yellow_text('PRINT_TIMESTAMP setting not found. Disabling.'))
    settings.PRINT_TIMESTAMP = False

if not hasattr(settings, 'PRINT_API_RESPONSE_SUMMARY'):
    print(yellow_text('PRINT_API_RESPONSE_SUMMARY setting not found. Disabling.'))
    settings.PRINT_API_RESPONSE_SUMMARY = False

# Validate required settings.py variables
required_settings = [
    'PREFERRED_APPLICATION_ONLY',
    'PREFERRED_PLAN_ONLY',
    'PREFERRED_REGION_ONLY',
    'PREFERRED_OS_ONLY',
    'INSTANCE_TAGS',
    'EMAIL_INSTANCE_CREATION']
missing_settings = [v for v in required_settings if not hasattr(settings, v)]
if missing_settings:
    print(red_text('Missing required settings variables: {', '.join(missing_settings)}. EXITING!'))
    exit(1)

# Check if preferred IDs exist
if not hasattr(settings, 'PREFERRED_APPLICATION_IDS'):
    print(yellow_text('PREFERRED_APPLICATION_IDS not defined '))
    settings.PREFERRED_APPLICATION_IDS = []

if not hasattr(settings, 'PREFERRED_PLAN_IDS'):
    print(yellow_text('PREFERRED_PLAN_IDS not defined '))
    settings.PREFERRED_APPLICATION_IDS = []

if not hasattr(settings, 'PREFERRED_REGION_IDS'):
    print(yellow_text('PREFERRED_REGION_IDS not defined '))
    settings.PREFERRED_APPLICATION_IDS = []

if not hasattr(settings, 'PREFERRED_OS_IDS'):
    print(yellow_text('PREFERRED_OS_IDS not defined '))
    settings.PREFERRED_APPLICATION_IDS = []

BASE_DIR = Path(__file__).resolve().parent.parent # Set base directory

from api.vultr import Vultr
from api.cloudflare import Cloudflare
from menu import Menu

# Load APIs using keys from config file. Display main menu.
vultr_api = Vultr(str(os.getenv('VULTR_API_KEY')))
cloudflare_api = Cloudflare(str(os.getenv('CLOUDFLARE_EMAIL')), str(os.getenv('CLOUDFLARE_API_KEY')))
menu = Menu(vultr_api, cloudflare_api)
menu.main_menu()
