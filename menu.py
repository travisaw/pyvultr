
from api.vultr import Vultr
from api.digitalocean import DigitalOcean
from api.cloudflare import Cloudflare
from vultrmenu import VultrMenu
from digitaloceanmenu import DigitalOceanMenu
from util import print_input_menu, print_text_prompt


class Menu():
    """

    """

    def __init__(self, api_keys):
        """
        """
        # Load APIs using keys from config file. Display main menu.
        self.vultr_api = Vultr(api_keys['vultr_api_key'])
        self.digitalocean_api = DigitalOcean(api_keys['vultr_api_key'])
        self.cloudflare_api = Cloudflare(api_keys['cloudflare_email'], api_keys['cloudflare_api_key'])

    def main_menu(self):
        """
        """
        options = [
            {'id': 1, 'name': 'Vultr'},
            {'id': 2, 'name': 'Digital Ocean'},
            {'id': 3, 'name': 'Exit'},
        ]
        option, inst_list = print_input_menu(options, 'What provider?: ', 'id', ['name'], False)
        match option:
            case '1':
                self.vultr()
            case '2':
                self.digitalocean()
            case '3':
                exit()


    def vultr(self):
        vultrmenu = VultrMenu(self.vultr_api, self.cloudflare_api)
        vultrmenu.main_menu()

    def digitalocean(self):
        digitalocean = DigitalOceanMenu(self.digitalocean_api, self.cloudflare_api)
        digitalocean.main_menu()
