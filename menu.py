
from endpoints.vultr.account import get_account_info
from endpoints.vultr.application import Application
from endpoints.vultr.instance import Instance
from endpoints.vultr.firewall import Firewall
from endpoints.vultr.os import OS
from endpoints.vultr.plan import Plan
from endpoints.vultr.region import Region
from endpoints.vultr.snapshot import Snapshot
from endpoints.cloudflare.zone import Zone
from endpoints.ipify import Ipify
from util import print_input_menu, print_text_prompt

class Menu():
    """
    Menu class provides a command-line interface for managing Vultr and Cloudflare resources.
    This class encapsulates the logic for displaying interactive menus and handling user input
    to perform various operations related to Vultr compute instances, firewalls, snapshots, and
    Cloudflare DNS zones. It initializes and manages the required API client objects and their
    associated resource managers.
        vultr_api: Instance of the Vultr API client.
        cloudflare_api: Instance of the Cloudflare API client.
        obj_fw: Firewall manager object for Vultr.
        obj_p: Plan manager object for Vultr compute plans.
        obj_r: Region manager object for Vultr regions.
        obj_ss: Snapshot manager object for Vultr snapshots.
        obj_cf: Zone manager object for Cloudflare DNS zones.
        obj_i: Instance manager object for Vultr compute instances.
    Methods:
        __init__(vultr_api, cloudflare_api):
            Initializes the Menu with Vultr and Cloudflare API clients and resource managers.
        main_menu():
            Displays the main menu and routes user selection to the appropriate submenu.
        account():
            Displays the Vultr account menu and handles account-related actions.
        instance():
            Displays the Vultr compute instance menu and handles instance management actions.
        firewall():
            Displays the Vultr firewall menu and handles firewall and rule management actions.
        snapshot():
            Displays the Vultr snapshot menu and handles snapshot management actions.
        dns_zone():
            Displays the Cloudflare DNS zone menu and handles DNS record management actions.
    """

    def __init__(self, vultr_api, cloudflare_api):
        """
        Initializes the main menu with API objects for Vultr and Cloudflare services.

        Args:
            vultr_api: An instance of the Vultr API client.
            cloudflare_api: An instance of the Cloudflare API client.

        Attributes:
            vultr_api: Stores the Vultr API client instance.
            cloudflare_api: Stores the Cloudflare API client instance.
            obj_fw: Firewall object initialized with the Vultr API.
            obj_p: Plan object for Vultr compute plans.
            obj_r: Region object for Vultr regions.
            obj_ss: Snapshot object for Vultr snapshots.
            obj_cf: Zone object for Cloudflare zones.
            obj_i: Instance object for Vultr compute instances, initialized with dependencies.
        """
        self.vultr_api = vultr_api                # Vultr API Object
        self.cloudflare_api = cloudflare_api      # Cloudflare API Object
        self.obj_ip = Ipify()                     # Ipify Zone Object
        self.obj_fw = Firewall(self.vultr_api, self.obj_ip) # Firewall Object
        self.obj_r = Region(self.vultr_api)       # Vultr Region Object
        self.obj_p = Plan(self.vultr_api, self.obj_r) # Vultr Compute Plan Object
        self.obj_ss = Snapshot(self.vultr_api)    # Vultr Snapshot Object
        self.obj_os = OS(self.vultr_api)          # Initialize Operating System Object
        self.obj_ap = Application(self.vultr_api) # Initialize Application Object
        self.obj_cf = Zone(self.cloudflare_api)   # Cloudflare Zone Object
        self.obj_i = Instance(self.vultr_api, self.obj_fw, self.obj_ss, self.obj_cf, self.obj_p, self.obj_r, self.obj_os, self.obj_ap) # Vultr Compute Instance Object

    def main_menu(self):
        """
        Displays the main menu for the application and handles user selection.

        Presents a list of options to the user, including Account, Instances, Firewall, Snapshot, DNS Zones, and Exit.
        Based on the user's input, calls the corresponding method to handle the selected area or exits the application.
        """
        options = [
            {'id': 1, 'name': 'Account'},
            {'id': 2, 'name': 'Instances'},
            {'id': 3, 'name': 'Firewall'},
            {'id': 4, 'name': 'Snapshot'},
            {'id': 5, 'name': 'Compute Regions'},
            {'id': 6, 'name': 'Compute Plans'},
            {'id': 7, 'name': 'Operating Systems'},
            {'id': 8, 'name': 'Applications'},
            {'id': 9, 'name': 'DNS Zones'},
            {'id': 10, 'name': 'Other'},
            {'id': 11, 'name': 'Exit'},
        ]
        option, inst_list = print_input_menu(options, 'What area?: ', 'id', ['name'], False)
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
                self.regions()
            case '6':
                self.plans()
            case '7':
                self.os()
            case '8':
                self.applications()
            case '9':
                self.dns_zone()
            case '10':
                self.other()
            case '11':
                exit()

    def account(self):
        """
        Displays the Vultr Account Menu, allowing the user to choose between showing account details or going back to the main menu.
        Handles user input and invokes the appropriate action based on the selected option.
        """
        options = [
            {'id': 1, 'name': 'Show Account Details'},
            {'id': 2, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', ['name'], False)
        match option:
            case '1':
                get_account_info(self.vultr_api)
                self.account()
            case '2':
                self.main_menu()

    def instance(self):
        """
        Displays the Vultr Compute Instance Menu and handles user actions.

        This method presents a menu of options related to managing Vultr compute instances,
        including showing all instances, showing a specific instance, creating or deleting
        instances, managing DNS names for IPv4/IPv6, and navigating back to the main menu.
        Based on the user's selection, the corresponding action is performed and the menu
        is displayed again until the user chooses to go back.

        Menu Options:
            1. Show Instances - List all compute instances.
            2. Show Instance - Display details for a specific instance.
            3. Create Instance - Prompt to create a new compute instance.
            4. Delete Instance - Delete an existing compute instance.
            5. Create IP4 DNS Name from Hostname - Create a DNS name for an IPv4 address.
            6. Create IP6 DNS Name from Hostname - Create a DNS name for an IPv6 address.
            7. Delete IP4 DNS Name - Delete a DNS name for an IPv4 address.
            8. Go Back - Return to the main menu.
        """
        options = [
            {'id': 1, 'name': 'Show Instances'},
            {'id': 2, 'name': 'Show Instance'},
            {'id': 3, 'name': 'Create Instance'},
            {'id': 4, 'name': 'Delete Instance'},
            {'id': 5, 'name': 'Update Firewall'},
            {'id': 6, 'name': 'Create IP4 DNS Name from Hostname'},
            {'id': 7, 'name': 'Create IP6 DNS Name from Hostname'},
            {'id': 8, 'name': 'Delete IP4 DNS Name'},
            {'id': 9, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', ['name'], False)
        match option:
            case '1':
                self.obj_i.get_instances()
                self.instance()
            case '2':
                self.obj_i.print_instance()
                self.instance()
            case '3':
                self.obj_i.create_instance_prompt()
                self.instance()
            case '4':
                self.obj_i.delete_instance()
                self.instance()
            case '5':
                self.obj_i.update_firewall()
                self.instance()
            case '6':
                self.obj_i.dns_from_hostname_ip4()
                self.instance()
            case '7':
                self.obj_i.dns_from_hostname_ip6()
                self.instance()
            case '8':
                self.obj_i.delete_dns(True)
                self.instance()
            case '9':
                self.main_menu()

    def firewall(self):
        """
        Displays the Vultr Firewall Menu and handles user interactions for firewall management.

        This method presents a menu with options to show, create, or delete firewalls and firewall rules,
        as well as to add the current IP to firewall rules. Based on the user's selection, it calls the
        corresponding methods from the firewall object (`self.obj_fw`). The menu loops after each action
        until the user chooses to go back to the main menu.

        Menu Options:
            1. Show Firewalls
            2. Show Selected Firewall
            3. Create Firewall
            4. Delete Firewall
            5. Show Firewall Rules
            6. Delete All Firewall Rules
            7. Add Current IP to Firewall Rules
            8. Go Back to Main Menu
        """
        options = [
            {'id': 1, 'name': 'Show Firewalls'},
            {'id': 2, 'name': 'Show Selected Firewall'},
            {'id': 3, 'name': 'Create Firewall'},
            {'id': 4, 'name': 'Delete Firewall'},
            {'id': 5, 'name': 'Show Firewall Rules'},
            {'id': 6, 'name': 'Delete All Firewall Rules'},
            {'id': 7, 'name': 'Delete Firewall Rules by Note'},
            {'id': 8, 'name': 'Add Current IP4 to Firewall Rules'},
            {'id': 9, 'name': 'Add Current IP6 to Firewall Rules'},
            {'id': 10, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', ['name'], False)
        match option:
            case '1':
                self.obj_fw.get_firewalls()
                self.firewall()
            case '2':
                self.obj_fw.print_firewall()
                self.firewall()
            case '3':
                self.obj_fw.create_firewall_prompt()
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
                self.obj_fw.delete_firewall_rule_with_notes()
                self.firewall()
            case '8':
                self.obj_fw.add_ip4_to_firewall_rules()
                self.firewall()
            case '9':
                self.obj_fw.add_ip6_to_firewall_rules()
                self.firewall()
            case '10':
                self.main_menu()

    def snapshot(self):
        """
        Displays the Vultr Snapshot Menu and handles user interactions for snapshot management.

        This method presents a menu with options to show all snapshots, show a selected snapshot,
        create a new snapshot, delete a snapshot, update a snapshot, or return to the main menu.
        Based on the user's selection, it calls the appropriate methods from the snapshot object
        (`self.obj_ss`) or navigates back to the main menu.

        Menu Options:
            1. Show Snapshots - Lists all available snapshots.
            2. Show Selected Snapshot - Displays details of a selected snapshot.
            3. Create Snapshot - Prompts for a name and creates a new snapshot for the current instance.
            4. Delete Snapshot - Deletes a selected snapshot.
            5. Update Snapshot - Prompts for a new name and updates a selected snapshot.
            6. Go Back - Returns to the main menu.
        """
        options = [
            {'id': 1, 'name': 'Show Snapshots'},
            {'id': 2, 'name': 'Show Selected Snapshot'},
            {'id': 3, 'name': 'Create Snapshot'},
            {'id': 4, 'name': 'Delete Snapshot'},
            {'id': 5, 'name': 'Update Snapshot'},
            {'id': 6, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', ['name'], False)
        match option:
            case '1':
                self.obj_ss.get_snapshots()
                self.snapshot()
            case '2':
                self.obj_ss.get_snapshot()
                self.snapshot()
            case '3':
                ss_name = print_text_prompt("New snapshot Name?: ")
                self.obj_ss.create_snapshot(ss_name, self.obj_i.instance_id)
                self.snapshot()
            case '4':
                self.obj_ss.delete_snapshot()
                self.snapshot()
            case '5':
                ss_name = print_text_prompt("New snapshot Name?: ")
                self.obj_ss.update_snapshot(ss_name)
                self.snapshot()
            case '6':
                self.main_menu()

    def regions(self):
        """
        Displays a menu for region-related actions and handles user selection.
        The menu provides the following options:
            1. Save Compute Regions: Saves the current compute regions using obj_r.save_regions().
            2. Show Selected Compute Region: Displays the preferred compute region using obj_r.get_preferred_region().
            3. Print All Regions: Prints all available regions using obj_r.print_all_regions().
            4. Print Preferred Regions: Prints the preferred regions using obj_r.print_preferred_regions().
            5. Go Back: Returns to the main menu.
        After performing the selected action, the method either redisplays the regions menu or returns to the main menu.
        """
        options = [
            {'id': 1, 'name': 'Save Compute Regions'},
            {'id': 2, 'name': 'Show Selected Compute Region'},
            {'id': 3, 'name': 'Select From All Regions'},
            {'id': 4, 'name': 'Select From Preferred Regions'},
            {'id': 5, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', ['name'], False)
        match option:
            case '1':
                self.obj_r.save_regions()
                self.regions()
            case '2':
                self.obj_r.print_region()
                self.regions()
            case '3':
                self.obj_r.get_all_region()
                self.regions()
            case '4':
                self.obj_r.get_preferred_region()
                self.regions()
            case '5':
                self.main_menu()

    def plans(self):
        """
        Displays the Vultr Compute Plans Menu and handles user interactions for managing compute plans.

        This method presents a menu with options to show all compute plans, show details of a selected plan,
        and return to the main menu. Based on the user's selection, it calls the appropriate methods from the
        Plan object (`self.obj_p`) or navigates back to the main menu.

        Menu Options:
            1. Show All Compute Plans - Lists all available compute plans.
            2. Show Selected Compute Plan - Displays details of a selected compute plan.
            3. Go Back - Returns to the main menu.
        """
        options = [
            {'id': 1, 'name': 'Save Compute Plans'},
            {'id': 2, 'name': 'Show Selected Compute Plan'},
            {'id': 3, 'name': 'Select From All Plans'},
            {'id': 4, 'name': 'Select From Preferred Plans'},
            {'id': 5, 'name': 'Select From Region Plans'},
            {'id': 6, 'name': 'Select From Regions Preferred Plans'},
            {'id': 7, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', ['name'], False)
        match option:
            case '1':
                self.obj_p.save_plans()
                self.plans()
            case '2':
                self.obj_p.print_plan()
                self.plans()
            case '3':
                self.obj_p.select_all_plans()
                self.plans()
            case '4':
                self.obj_p.select_preferred_plans()
                self.plans()
            case '5':
                self.obj_p.select_region_plans()
                self.plans()
            case '6':
                self.obj_p.select_preferred_region_plans()
                self.plans()
            case '7':
                self.main_menu()

    def os(self):
        """
        Displays an operating system (OS) management menu and handles user actions.

        Presents a menu with the following options:
            1. Save OS: Saves the currently selected OS.
            2. Show Selected OS: Displays information about the selected OS.
            3. Select From All OS: Allows the user to select an OS from all available options.
            4. Select From Preferred OS: Allows the user to select an OS from a list of preferred options.
            5. Go Back: Returns to the main menu.

        The method loops after each action until the user chooses to go back.
        """
        options = [
            {'id': 1, 'name': 'Save OS'},
            {'id': 2, 'name': 'Show Selected OS'},
            {'id': 3, 'name': 'Select From All OS'},
            {'id': 4, 'name': 'Select From Preferred OS'},
            {'id': 5, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', ['name'], False)
        match option:
            case '1':
                self.obj_os.save_os()
                self.os()
            case '2':
                self.obj_os.print_os()
                self.os()
            case '3':
                self.obj_os.get_all_os()
                self.os()
            case '4':
                self.obj_os.get_preferred_os()
                self.os()
            case '5':
                self.main_menu()

    def applications(self):
        """
        Displays a menu for application-related actions and handles user selection.

        Presents the user with a list of options to save applications, show the selected application,
        select from all applications, select from preferred applications, or go back to the main menu.
        Executes the corresponding method based on the user's choice and loops back to the menu
        unless the user chooses to go back.

        Returns:
            None
        """
        options = [
            {'id': 1, 'name': 'Save Applications'},
            {'id': 2, 'name': 'Show Selected Application'},
            {'id': 3, 'name': 'Select From All Applications'},
            {'id': 4, 'name': 'Select From Preferred Applications'},
            {'id': 5, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', ['name'], False)
        match option:
            case '1':
                self.obj_ap.save_applications()
                self.applications()
            case '2':
                self.obj_ap.print_application()
                self.applications()
            case '3':
                self.obj_ap.get_all_applications()
                self.applications()
            case '4':
                self.obj_ap.get_preferred_applications()
                self.applications()
            case '5':
                self.main_menu()

    def dns_zone(self):
        """
        Displays and manages the Cloudflare DNS Zone menu, allowing the user to perform various DNS-related actions.

        Menu options include:
            1. Show all available DNS zones.
            2. Show details of the currently selected DNS zone.
            3. Show DNS records for the selected zone.
            4. Select a DNS record of type A or AAAA.
            5. Show details for the selected DNS record.
            6. Create a new DNS record.
            7. Delete an existing DNS record.
            8. Verify authentication tokens.
            9. Return to the main menu.

        Each option invokes the corresponding method from the Cloudflare object (`self.obj_cf`) and then redisplays the menu, except for "Go Back", which returns to the main menu.
        """
        options = [
            {'id': 1, 'name': 'Show Zones'},
            {'id': 2, 'name': 'Show Selected Zone'},
            {'id': 3, 'name': 'Show Zone DNS Records'},
            {'id': 4, 'name': 'Select Zone DNS Record (A and AAAA only)'},
            {'id': 5, 'name': 'Show DNS Record Details'},
            {'id': 6, 'name': 'Create DNS Record'},
            {'id': 7, 'name': 'Delete DNS Record'},
            {'id': 8, 'name': 'Verify Tokens'},
            {'id': 9, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', ['name'], False)
        match option:
            case '1':
                self.obj_cf.get_zones()
                self.dns_zone()
            case '2':
                self.obj_cf.print_zone()
                self.dns_zone()
            case '3':
                self.obj_cf.print_dns_records()
                self.dns_zone()
            case '4':
                self.obj_cf.get_dns_record_of_type(['A', 'AAAA',])
                self.dns_zone()
            case '5':
                self.obj_cf.print_dns_record()
                self.dns_zone()
            case '6':
                self.obj_cf.create_dns_record_prompt()
                self.dns_zone()
            case '7':
                self.obj_cf.delete_dns_record()
                self.dns_zone()
            case '8':
                self.obj_cf.verify_token()
                self.dns_zone()
            case '9':
                self.main_menu()

    def other(self):
        """
        Displays a menu with additional options for the user, such as viewing their IP address or returning to the main menu.
        Presents the user with a list of actions:
            1. Display the user's IP address by calling `self.obj_ip.print_ip()` and then redisplays this menu.
            2. Return to the main menu by calling `self.main_menu()`.
        Utilizes `print_input_menu` to render the menu and handle user input.
        """
        options = [
            {'id': 1, 'name': 'My IP Address'},
            {'id': 2, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', ['name'], False)
        match option:
            case '1':
                self.obj_ip.print_ip()
                self.other()
            case '2':
                self.main_menu()
