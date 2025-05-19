
from endpoints.account import get_account_info
from endpoints.instance import get_instances
from endpoints.firewall import Firewall

class Menu():
    def __init__(self, api):
        self.api = api
        self.obj_fw = Firewall(self.api)

    def main_menu(self):
        print('1. Account')
        print('2. Instances')
        print('3. Firewall')
        print('4. Exit')
        option = input("What area?: ")
        match option:
            case '1':
                self.account()
            case '2':
                self.instance()
            case '3':
                self.firewall()
            case '4':
                exit()
            case _:
                print('Invalid Option!')
                self.main_menu()

    def account(self):
        print('1. Show Account Details')
        print('2. Go Back')
        option = input("What action?: ")
        match option:
            case '1':
                get_account_info(self.api)
                self.account()
            case '2':
                self.main_menu()
            case _:
                print('Invalid Option!')
                self.account()

    def instance(self):
        print('1. Show Instances')
        print('2. Go Back')
        option = input("What action?: ")
        match option:
            case '1':
                get_instances(self.api)
                self.instances()
            case '2':
                self.main_menu()
            case _:
                print('Invalid Option!')
                self.instances()

    def firewall(self):
        print('1. Show Firewalls')
        print('2. Show Selected Firewall')
        print('3. Create Firewall')
        print('4. Delete Firewall')
        print('5. Show Firewall Rules')
        print('6. Delete All Firewall Rules')
        print('7. Add Current IP to Firewall Rules')
        print('8. Go Back')
        option = input("What area?: ")
        match option:
            case '1':
                self.obj_fw.get_firewalls()
                self.firewall()
            case '2':
                self.obj_fw.get_firewall()
                self.firewall()
            case '3':
                fw_name = input("New Firewall Name?: ")
                self.obj_fw.create_firewall(fw_name)
                self.firewall()
            case '4':
                self.obj_fw.delete_firewall()
                self.firewall()
            case '5':
                self.obj_fw.get_firewall_rules()
                self.firewall()
            case '6':
                self.obj_fw.delete_all_firewall_rules()
                self.firewall()
            case '7':
                self.obj_fw.add_ip_to_firewall_rules()
                self.firewall()
            case '8':
                self.main_menu()
            case _:
                print('Invalid Option!')
                self.instances()

                