
from endpoints.account import get_account_info
from endpoints.instance import get_instances
from endpoints.firewall import get_firewalls

class Menu():
    def __init__(self, api):
        self.api = api

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
        print('2. Go Back')
        option = input("What area?: ")
        match option:
            case '1':
                get_firewalls(self.api)
                self.firewall()
            case '2':
                self.main_menu()
            case _:
                print('Invalid Option!')
                self.instances()