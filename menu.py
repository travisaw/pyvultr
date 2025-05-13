
from account import get_account_info

class Menu():
    def __init__(self, api):
        self.api = api

    def main_menu(self):
        print('1. Account')
        print('2. Firewall')
        print('3. Exit')
        option = input("What area?: ")
        match option:
            case '1':
                self.account()
            case '2':
                print('Coming Soon!')
                self.main_menu()
            case '3':
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
