
from endpoints.account import get_account_info
from endpoints.instances import get_instances

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
                self.instances()
            case '3':
                print('Coming Soon!')
                self.main_menu()
            case '4':
                exit()
            case _:
                print('Invalid Option!')
                self.main_menu()

    def account(self):
        print('1. Show Account Details')
        print('2. Go Back')
        option = input("What area?: ")
        match option:
            case '1':
                get_account_info(self.api)
                self.account()
            case '2':
                self.main_menu()
            case _:
                print('Invalid Option!')
                self.account()

    def instances(self):
        print('1. Show Instances')
        print('2. Go Back')
        option = input("What area?: ")
        match option:
            case '1':
                get_instances(self.api)
                self.instances()
            case '2':
                self.main_menu()
            case _:
                print('Invalid Option!')
                self.instances()
