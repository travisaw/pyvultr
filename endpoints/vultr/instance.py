from util import utc_str_to_local, print_input_menu, valid_response_vultr, print_output_table, format_currency, print_yes_no, hour_minutee_day_diff
from data import load_cloud_init
from colorama import Fore, Style
from colorama import init as colorama_init
import settings

class Instance:
    """
    Represents a Vultr compute instance and provides methods to manage its lifecycle and related resources.
    The `Instance` class encapsulates operations for interacting with Vultr compute instances, including fetching, displaying, creating, and deleting instances, as well as managing associated DNS records and firewall settings. It integrates with various helper objects for API communication, firewall management, snapshot handling, Cloudflare DNS, region selection, and more.
    Attributes:
        instance_id (str): The unique identifier of the selected instance.
        instance_tags (list): Tags associated with the instance.
        instance_hostname (str): Hostname of the instance.
        instance_ip4 (str): Main IPv4 address of the instance.
        instance_ip6 (str): Main IPv6 address of the instance.
        api: API client object for Vultr API communication.
        fw_obj: Firewall management object.
        ss_obj: Snapshot management object.
        cf_obj: Cloudflare DNS management object.
        p_obj: Additional helper object (purpose defined elsewhere).
        r_obj: Region management object.
    Methods:
        get_instances():
            Fetches all Vultr compute instances, prompts the user to select one, and loads its details.
        get_instance():
            Retrieves and updates details for the currently selected instance.
        print_instance():
            Prints detailed information about the selected instance in a tabular format.
        create_instance_prompt():
            Prompts the user for details and initiates the creation of a new instance.
        create_instance(body):
            Creates a new instance using the provided configuration.
        delete_instance():
            Deletes the current instance if it is not tagged as production.
        dns_from_hostname_ip4():
            Creates an A record in Cloudflare DNS for the instance's IPv4 address.
        dns_from_hostname_ip6():
            Placeholder for creating an AAAA record for the instance's IPv6 address.
        delete_dns(ip4):
            Deletes the DNS record for the instance's hostname and IP address.
        __instance_status_color(status):
            Returns a colorized string for the instance's status.
        __instance_power_status_color(status):
            Returns a colorized string for the instance's power status.
        __instance_server_status_color(status):
            Returns a colorized string for the instance's server status.
        __is_instance_prod():
            Checks if the instance is tagged as production and prevents destructive actions if so.
    """
    instance_id = str('')
    instance_tags = []
    instance_hostname = ''
    instance_ip4 = ''
    instance_ip6 = ''

    def __init__(self, api, fw_obj, ss_obj, cf_obj, p_obj, r_obj, os_obj):
        """
        Initializes the instance with required API and object dependencies.

        Args:
            api: The API client or interface used for making requests.
            fw_obj: Firewall object for managing firewall configurations.
            ss_obj: Snapshot object for handling instance snapshots.
            cf_obj: Configuration object for instance settings.
            p_obj: Plan object representing instance plans.
            r_obj: Region object specifying instance regions.
            os_obj: Operating system object for managing OS-related operations.
        """
        self.api = api
        self.fw_obj = fw_obj
        self.ss_obj = ss_obj
        self.cf_obj = cf_obj
        self.p_obj = p_obj
        self.r_obj = r_obj
        self.os_obj = os_obj
        colorama_init(autoreset=True)

    def get_instances(self):
        """
        Fetches all Vultr compute instances and prompts the user to select one.

        Retrieves the list of instances from the Vultr API, displays them in a menu for user selection,
        sets the selected instance's ID, and loads its details into the object's attributes.
        """
        url = 'instances'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            option, inst_list = print_input_menu(data['instances'], 'What instance to select?: ', 'id', ['label'], True)
            self.instance_id = inst_list[int(option)][0]
            self.get_instance()

    def get_instance(self):
        """
        Retrieves details for the current instance from the Vultr API and updates instance attributes.

        Fetches instance information such as tags, hostname, IPv4, and IPv6 addresses using the instance ID.
        Updates the following attributes if the API response is valid:
            - instance_tags: List of tags associated with the instance.
            - instance_hostname: Hostname of the instance.
            - instance_ip4: Main IPv4 address of the instance.
            - instance_ip6: Main IPv6 address of the instance.

        Returns:
            None
        """
        url = f'instances/{self.instance_id}'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            self.instance_tags = data['instance']['tags']
            self.instance_hostname = data['instance']['hostname']
            self.instance_ip4 = data['instance']['main_ip']
            self.instance_ip6 = data['instance']['v6_main_ip']

    def print_instance(self):
        """
        Prints detailed information about the currently selected Vultr instance in a tabular format.

        This method retrieves instance details from the Vultr API using the instance ID, fetches associated firewall information,
        and displays various attributes such as label, hostname, region, OS, hardware specs, IP addresses, firewall group, status, and more.
        If no instance is selected, it notifies the user.

        Requirements:
            - self.instance_id: The ID of the instance to display.
            - self.api.api_get: Method to perform a GET request to the Vultr API.
            - valid_response_vultr: Function to validate the API response.
            - self.fw_obj: Firewall object with 'firewall_id', 'get_firewall()', and 'firewall_desc' attributes.
            - tabulate: Function to format data in a table.
            - utc_str_to_local: Function to convert UTC date strings to local time.
            - __instance_status_color, __instance_power_status_color, __instance_server_status_color: Methods to colorize status fields.

        Prints:
            - A table of instance details if an instance is selected and the API response is valid.
            - 'No Instance Selected!' if no instance is selected.
        """
        if self.instance_id != '':
            url = f'instances/{self.instance_id}'
            data = self.api.api_get(url)
            if valid_response_vultr(data):
                self.fw_obj.firewall_id = data['instance']['firewall_group_id']
                self.fw_obj.get_firewall()
                output = [
                    ['Label', data['instance']['label']],
                    ['Hostname', data['instance']['hostname']],
                    ['Tags', data['instance']['tags']],
                    ['Region', self.r_obj.city_from_id(data['instance']['region'])],
                    ['Date Created', utc_str_to_local(data['instance']['date_created'])],
                    ['Duration', hour_minutee_day_diff(data['instance']['date_created'])],
                    ['Plan', data['instance']['plan']],
                    ['OS', data['instance']['os']],
                    ['OS ID', data['instance']['os_id']],
                    ['App Id', data['instance']['app_id']],
                    ['vCPU Count', data['instance']['vcpu_count']],
                    ['Ram', data['instance']['ram']],
                    ['Disk', data['instance']['disk']],
                    ['Allowed Bandwidth', data['instance']['allowed_bandwidth']],
                    # ['internal_ip', data['instance']['internal_ip']],
                    # ['netmask_v4', data['instance']['netmask_v4']],
                    ['v4 Main IP', data['instance']['main_ip']],
                    # ['gateway_v4', data['instance']['gateway_v4']],
                    # ['v6_network', data['instance']['v6_network']],
                    ['v6 Main IP', data['instance']['v6_main_ip']],
                    # ['v6_network_size', data['instance']['v6_network_size']],
                    ['Firewall Group', self.fw_obj.firewall_desc],
                    ['Status', self.__instance_status_color(data['instance']['status'])],
                    ['Power Status', self.__instance_power_status_color(data['instance']['power_status'])],
                    ['Server Status', self.__instance_server_status_color(data['instance']['server_status'])],
                    # ['image_id', data['instance']['image_id']],
                    ['Features', data['instance']['features']],
                    ['User Scheme', data['instance']['user_scheme']],
                    ['Pending Charges', format_currency(data['instance']['pending_charges'])],
                ]
                print_output_table(output)
        else:
            print('No Instance Selected!')

    def create_instance_prompt(self):
        """
        Prompts the user for instance creation details and initiates the creation process.

        This method interacts with the user to obtain a hostname/label for the new instance,
        retrieves preferred region, available firewalls, and snapshots, then constructs the
        request body with these details and default values for other parameters. Finally,
        it calls the method to create the instance with the assembled configuration.

        Prompts:
            - Hostname/Label for the new instance.

        Side Effects:
            - Calls methods to fetch preferred region, firewalls, and snapshots.
            - Initiates the creation of a new instance using the collected information.
        """
        # Prompt for hostname/label
        label = input('Hostname/Label?:')

        # Select region and plans
        if settings.PREFERRED_REGION_ONLY:
            self.r_obj.get_preferred_region()
        else:
            self.r_obj.get_all_region()
        
        if settings.PREFERRED_PLAN_ONLY:
            print('Using preferred plans only.')
            self.p_obj.select_preferred_region_plans(False)
        else:
            print('Using all plans.')
            self.p_obj.select_region_plans(False)

        body = {
            "region": self.r_obj.region_id,
            "plan": self.p_obj.plan_id,
            "label": label,
            "hostname": label,
            "tags": settings.INSTANCE_TAGS,
            "enable_private_network": "false",
            "enable_ipv6": "false",
        }

        # Select Firewall
        self.fw_obj.get_firewalls()
        if self.fw_obj.firewall_selected():
            body['firewall_group_id'] = self.fw_obj.firewall_id

        # Select OS Source
        os_source = [
            {'id': '1', 'name': 'Snapshot'},
            {'id': '2', 'name': 'Blank OS'},
        ]
        option, r_list = print_input_menu(os_source, 'What OS to use?: ', 'id', ['name'], False)
        match r_list[int(option) - 1][0]:
            case '1':
                self.ss_obj.get_snapshots()
                body['snapshot_id'] = self.ss_obj.snapshot_id
            case '2':
                if settings.PREFERRED_OS_ONLY:
                    self.os_obj.get_preferred_os()
                else:
                    self.os_obj.get_all_os()
                body['os_id'] = self.os_obj.os_id

                # Load cloud-init configuration if available
                if print_yes_no('Use Cloud Init?'):
                    body['user_data'] = load_cloud_init('default.yml')

        # Send activation email if enabled
        if settings.EMAIL_INSTANCE_CREATION:
            body['activation_email'] = "true"

        self.create_instance(body)

    def create_instance(self, body):
        """
        Creates a new instance using the provided request body.

        Args:
            body (dict): The request payload containing instance configuration parameters.

        Returns:
            None

        Side Effects:
            - Sends a POST request to the 'instances' endpoint.
            - If the response is valid, sets `self.instance_id` to the new instance's ID and calls `self.get_instance()`.

        Prints:
            - 'Instance created and selected' if the instance is successfully created and selected.
        """
        url = 'instances'
        data = self.api.api_post(url, body)
        if valid_response_vultr(data):
            print('Instance created and selected')
            self.instance_id = data['instance']['id']
            self.get_instance()

    def delete_instance(self):
        """
        Deletes the current instance if it is not a production instance.

        This method checks whether the instance is marked as production using the
        `__is_instance_prod` method. If it is, the deletion is aborted. Otherwise,
        it sends a DELETE request to the API to remove the instance. If the API
        response is valid, it prints the status and additional information.

        Returns:
            None
        """
        if self.__is_instance_prod():
            return
        url = f'instances/{self.instance_id}'
        data = self.api.api_delete(url)
        if valid_response_vultr(data):
            print(f" {data['status']}: {data['info']}")

    def update_firewall(self):
        """
        Updates the firewall settings for the current instance.

        This method retrieves the current firewall settings and prompts the user to select a new firewall group.
        If a valid selection is made, it updates the instance's firewall group ID and prints a confirmation message.

        Returns:
            None
        """
        self.fw_obj.get_firewalls()
        url = f'instances/{self.instance_id}'
        body = {
            "firewall_group_id": None
        }
        data = self.api.api_patch(url, body)
        if valid_response_vultr(data):
            print(f"Firewall updated to {self.fw_obj.firewall_desc}")

    def dns_from_hostname_ip4(self):
        self.cf_obj.get_zones() # Select DNS zone
        if self.instance_ip4 == '0.0.0.0' or self.instance_ip4 == '':
            print('No IP address assigned yet.')
            return
        proxied = False
        if print_yes_no('DNS Proxied?'):
            proxied = True
        body = {
            "comment": "Added by pyvultr",
            "content": self.instance_ip4,
            "name": self.instance_hostname,
            "proxied": proxied,
            "ttl": 300,
            "type": "A"
        }
        self.cf_obj.create_update_dns_record(body)

    def dns_from_hostname_ip6(self):
        pass

    def delete_dns(self, ip4):
        """
        Deletes the DNS record associated with the instance's hostname and IP address.

        If the instance is in production, the method returns without making any changes.
        Depending on the `ip4` parameter, selects either the IPv4 or IPv6 address of the instance.
        Fetches the DNS zones and checks if a DNS record exists for the instance's hostname and selected IP.
        If such a DNS record exists, it is deleted.

        Args:
            ip4 (bool): If True, use the instance's IPv4 address; otherwise, use the IPv6 address.

        Returns:
            None
        """
        if self.__is_instance_prod():
            return
        if ip4:
            ip = self.instance_ip4
        else:
            ip = self.instance_ip6
        self.cf_obj.get_zones()
        if self.cf_obj.get_dns_record_by_name_content(self.instance_hostname, ip):
            self.cf_obj.delete_dns_record()

    def __instance_status_color(self, status):
        """
        Returns the status string colored according to its value using ANSI escape codes.

        Args:
            status (str): The status of the instance. Expected values are 'active', 'pending', 'suspended', or 'resizing'.

        Returns:
            str: The status string wrapped in color codes for terminal output. If the status is not recognized, returns the original status string without coloring.

        Color mapping:
            - 'active': Green
            - 'pending': Yellow
            - 'suspended': Red
            - 'resizing': Yellow
            - Any other value: No color
        """
        match status:
            case 'active':
                return f'{Fore.GREEN}{status}{Style.RESET_ALL}'
            case 'pending':
                return f'{Fore.YELLOW}{status}{Style.RESET_ALL}'
            case 'suspended':
                return f'{Fore.RED}{status}{Style.RESET_ALL}'
            case 'resizing':
                return f'{Fore.YELLOW}{status}{Style.RESET_ALL}'
            case _:
                return status

    def __instance_power_status_color(self, status):
        """
        Returns the power status string colored according to its value.

        Args:
            status (str): The power status of the instance. Expected values are 'running', 'stopped', or any other string.

        Returns:
            str: The status string colored green if 'running', red if 'stopped', or uncolored for any other status.
        """
        match status:
            case 'running':
                return f'{Fore.GREEN}{status}{Style.RESET_ALL}'
            case 'stopped':
                return f'{Fore.RED}{status}{Style.RESET_ALL}'
            case _:
                return status

    def __instance_server_status_color(self, status):
        """
        Returns a color-coded string representation of the server status using ANSI escape codes.

        Args:
            status (str): The status of the server. Expected values are 'none', 'locked', 'installingbooting', 'ok', or any other string.

        Returns:
            str: The status string wrapped in color codes based on its value:
                - Yellow for 'none' and 'installingbooting'
                - Red for 'locked'
                - Green for 'ok'
                - No color for any other status
        """
        match status:
            case 'none':
                return f'{Fore.YELLOW}{status}{Style.RESET_ALL}'
            case 'locked':
                return f'{Fore.RED}{status}{Style.RESET_ALL}'
            case 'installingbooting':
                return f'{Fore.YELLOW}{status}{Style.RESET_ALL}'
            case 'ok':
                return f'{Fore.GREEN}{status}{Style.RESET_ALL}'
            case _:
                return status

    def __is_instance_prod(self):
        """
        Checks if the instance is tagged as 'prod' (production).

        Returns:
            bool: True if 'prod' is present in the instance's tags, indicating a production resource; False otherwise.
            Prints a warning message if the instance is tagged as production.
        """
        if 'prod' in self.instance_tags:
            print(f"CANNOT DELETE RESOURCES TAGGED AS PRODUCTION")
            return True
        else:
            return False
