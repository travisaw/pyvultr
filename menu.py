
from endpoints.account import get_account_info
from endpoints.instance import Instance
from endpoints.firewall import Firewall
from endpoints.snapshot import Snapshot
from util import print_input_menu

class Menu():
    def __init__(self, api):
        self.api = api
        self.obj_fw = Firewall(self.api)
        self.obj_ss = Snapshot(self.api)
        self.obj_i = Instance(self.api, self.obj_fw, self.obj_ss)

    def main_menu(self):
        options = [
            {'id': 1, 'name': 'Account'},
            {'id': 2, 'name': 'Instances'},
            {'id': 3, 'name': 'Firewall'},
            {'id': 4, 'name': 'Snapshot'},
            {'id': 5, 'name': 'Exit'},
        ]
        option, inst_list = print_input_menu(options, 'What area?: ', 'id', 'name', False)
        match option:
            case '1':
                self.account()
            case '2':
                self.instance()
            case '3':
                self.firewall()
            case '4':
                self.snapshot()
            case '5':
                exit()

    def account(self):
        options = [
            {'id': 1, 'name': 'Show Account Details'},
            {'id': 2, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', 'name', False)
        match option:
            case '1':
                get_account_info(self.api)
                self.account()
            case '2':
                self.main_menu()

    def instance(self):
        options = [
            {'id': 1, 'name': 'Show Instances'},
            {'id': 2, 'name': 'Show Instance'},
            {'id': 3, 'name': 'Create Instance'},
            {'id': 4, 'name': 'Delete Instance'},
            {'id': 5, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', 'name', False)
        match option:
            case '1':
                self.obj_i.get_instances()
                self.instance()
            case '2':
                self.obj_i.print_instance()
                self.instance()
            case '3':
                self.obj_i.create_instance()
                self.instance()
            case '4':
                self.obj_i.delete_instance()
                self.instance()
            case '5':
                self.main_menu()

    def firewall(self):
        options = [
            {'id': 1, 'name': 'Show Firewalls'},
            {'id': 2, 'name': 'Show Selected Firewall'},
            {'id': 3, 'name': 'Create Firewall'},
            {'id': 4, 'name': 'Delete Firewall'},
            {'id': 5, 'name': 'Show Firewall Rules'},
            {'id': 6, 'name': 'Delete All Firewall Rules'},
            {'id': 7, 'name': 'Add Current IP to Firewall Rules'},
            {'id': 8, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', 'name', False)
        match option:
            case '1':
                self.obj_fw.get_firewalls()
                self.firewall()
            case '2':
                self.obj_fw.print_firewall()
                self.firewall()
            case '3':
                fw_name = input("New Firewall Name?: ")
                self.obj_fw.create_firewall(fw_name)
                self.firewall()
            case '4':
                self.obj_fw.delete_firewall()
                self.firewall()
            case '5':
                self.obj_fw.print_firewall_rules()
                self.firewall()
            case '6':
                self.obj_fw.delete_all_firewall_rules()
                self.firewall()
            case '7':
                self.obj_fw.add_ip_to_firewall_rules()
                self.firewall()
            case '8':
                self.main_menu()

    def snapshot(self):
        options = [
            {'id': 1, 'name': 'Show Snapshots'},
            {'id': 2, 'name': 'Show Selected Snapshot'},
            {'id': 3, 'name': 'Create Snapshot'},
            {'id': 4, 'name': 'Delete Snapshot'},
            {'id': 5, 'name': 'Update Snapshot'},
            {'id': 6, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', 'name', False)
        match option:
            case '1':
                self.obj_ss.get_snapshots()
                self.snapshot()
            case '2':
                self.obj_ss.get_snapshot()
                self.snapshot()
            case '3':
                ss_name = input("New snapshot Name?: ")
                self.obj_ss.create_snapshot(ss_name, self.obj_i.instance_id)
                self.snapshot()
            case '4':
                self.obj_ss.delete_snapshot()
                self.snapshot()
            case '5':
                ss_name = input("New snapshot Name?: ")
                self.obj_ss.update_snapshot(ss_name)
                self.snapshot()
            case '6':
                self.main_menu()
