from util import utc_str_to_local, print_input_menu, valid_response_vultr, print_output_table, print_text_prompt, yellow_text

class Firewall:
    """
    A class to manage Vultr firewall groups and their rules via the Vultr API.
    Attributes:
        firewall_id (str): The ID of the selected firewall group.
        firewall_desc (str): The description of the selected firewall group.
        firewall_rules (list): List of rules for the selected firewall group.
        firewall_rules_header (list): Column headers for displaying firewall rules.
    Methods:
        __init__(api):
            Initializes the Firewall object with the provided API client.
        get_firewalls():
            Retrieves all firewall groups, prompts the user to select one, and loads its rules.
        get_firewall():
            Retrieves and updates the description of the currently selected firewall group.
        print_firewall():
            Prints details of the currently selected firewall group.
        create_firewall_prompt():
            Prompts the user for a new firewall group name and creates it.
        create_firewall(body):
            Creates a new firewall group with the provided body.
        delete_firewall():
            Deletes the currently selected firewall group.
        get_firewall_rules():
            Retrieves and stores the rules for the currently selected firewall group.
        print_firewall_rules():
            Prints the rules of the currently selected firewall group.
        delete_all_firewall_rules():
            Deletes all rules from the currently selected firewall group.
        add_ip_to_firewall_rules():
            Adds rules for the current public IPv4 address to the selected firewall group.
        firewall_selected():
            Checks if a firewall group is selected; prints a message if not.
    Note:
        This class depends on external utility functions such as valid_response_vultr, print_input_menu, utc_str_to_local, and tabulate, as well as an API client with api_get, api_post, and api_delete methods.
    """
    firewall_id = str('')
    firewall_desc = str('')
    firewall_rules = []
    firewall_rules_header = ['Type', 'Action', 'Protocol', 'Ip', 'Port', 'Notes']
    firewall_rule_id = str('')

    def __init__(self, api, ipify):
        """
        Initialize the class with the provided API client.

        Args:
            api: An instance of the API client used to make requests.
        """
        self.api = api
        self.ipify = ipify

    def get_firewalls(self):
        """
        Retrieves the list of firewall groups from the Vultr API, presents them to the user for selection,
        and stores the selected firewall's ID and description as instance attributes. After selection,
        it calls `get_firewall_rules()` to retrieve the rules for the chosen firewall group.

        Returns:
            None

        Side Effects:
            - Sets `self.firewall_id` and `self.firewall_desc` based on user selection.
            - Calls `self.get_firewall_rules()` for the selected firewall group.
        """
        url = 'firewalls'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            option, fw_list = print_input_menu(data['firewall_groups'], 'What firewall to select?: ', 'id', ['description'], True)
            self.firewall_id = fw_list[int(option)][0]
            self.firewall_desc = fw_list[int(option)][1]
            self.get_firewall_rules()

    def get_firewall(self):
        """
        Retrieves the details of the currently selected firewall group from the Vultr API.

        If a firewall group is selected, this method sends a GET request to the Vultr API to fetch
        the firewall group's details. Upon receiving a valid response, it updates the instance's
        `firewall_desc` attribute with the firewall group's description.

        Returns:
            None

        Raises:
            Any exceptions raised by the underlying API call or response validation are propagated.
        """
        if self.firewall_selected():
            url = f'firewalls/{self.firewall_id}'
            data = self.api.api_get(url)
            if valid_response_vultr(data):
                self.firewall_desc = data['firewall_group']['description']

    def print_firewall(self):
        """
        Prints detailed information about the currently selected firewall group.

        This method retrieves the firewall group details from the Vultr API using the selected firewall ID.
        If the API response is valid, it displays the firewall group's description, creation and modification dates
        (converted to local time), instance count, rule count, and maximum rule count in a tabulated format.

        Returns:
            None
        """
        if self.firewall_selected():
            url = f'firewalls/{self.firewall_id}'
            data = self.api.api_get(url)
            if valid_response_vultr(data):
                result = [
                    ['Description: ', data['firewall_group']['description']],
                    ['Date Created: ', utc_str_to_local(data['firewall_group']['date_created'])],
                    ['Date Updated: ', utc_str_to_local(data['firewall_group']['date_modified'])],
                    ['Instance Count: ', data['firewall_group']['instance_count']],
                    ['Rule Count: ', data['firewall_group']['rule_count']],
                    ['Max Rule Count: ', data['firewall_group']['max_rule_count']]
                ]
                print_output_table(result)

    def create_firewall_prompt(self):
        """
        Prompts the user to enter a name for a new firewall, constructs a request body with the provided name,
        and calls the method to create the firewall.

        Returns:
            None
        """
        fw_name = print_text_prompt("New Firewall Name?: ")
        body = {'description': fw_name}
        self.create_firewall(body)

    def create_firewall(self, body):
        """
        Creates a new firewall group using the provided request body.

        Args:
            body (dict): The request payload containing firewall group details.

        Returns:
            None

        Side Effects:
            Sends a POST request to the 'firewalls' endpoint.
            Prints a confirmation message if the firewall group is created successfully.
        """
        url = 'firewalls'
        data = self.api.api_post(url, body)
        if valid_response_vultr(data):
            print(f" Created firewall '{data['firewall_group']['description']}'")

    def delete_firewall(self):
        """
        Deletes the firewall associated with this instance using the Vultr API.

        Sends a DELETE request to the Vultr API for the firewall identified by `self.firewall_id`.
        If the response is valid, prints the status and info returned by the API.

        Returns:
            None

        Raises:
            Any exceptions raised by the underlying API call or response validation.
        """
        if not self.firewall_selected():
            return
        url = f'firewalls/{self.firewall_id}'
        data = self.api.api_delete(url)
        if valid_response_vultr(data):
            print(f" {data['status']}: {data['info']}")

    def get_firewall_rules(self):
        """
        Retrieves the firewall rules for the currently selected firewall and stores them in the `firewall_rules` attribute.

        If a firewall is selected, this method sends a GET request to the Vultr API to fetch the rules associated with the selected firewall.
        The rules are processed and stored as a list of lists, where each inner list contains the following fields for a rule:
            - id
            - type
            - ip_type
            - action
            - protocol
            - port
            - subnet
            - subnet_size
            - source
            - notes

        If no firewall is selected, the `firewall_rules` attribute is set to an empty list.
        """
        if self.firewall_selected():
            url = f'firewalls/{self.firewall_id}/rules'
            data = self.api.api_get(url)
            if valid_response_vultr(data):
                result = []
                for i in data['firewall_rules']:
                    row = [
                        i['id'],
                        i['type'],
                        i['ip_type'],
                        i['action'],
                        i['protocol'],
                        i['port'],
                        i['subnet'],
                        i['subnet_size'],
                        i['source'],
                        i['notes'],
                    ]
                    result.append(row)
                self.firewall_rules = result
        else:
            self.firewall_rules = []

    def print_firewall_rules(self):
        """
        Retrieves and prints the firewall rules in a tabular format.

        This method calls `get_firewall_rules()` to update the list of firewall rules,
        formats each rule into a row with selected fields, and prints the result using
        the `tabulate` function with the specified headers.

        Returns:
            None
        """
        if not self.firewall_selected():
            return
        self.get_firewall_rules()
        result = []
        for i in self.firewall_rules:
            row = [
                i[1],
                i[3],
                i[4],
                i[6] + '/' + str(i[7]),
                i[5],
                i[9],
            ]
            result.append(row)
        print_output_table(result, self.firewall_rules_header)

    def delete_all_firewall_rules(self):
        """
        Deletes all firewall rules associated with the current firewall.

        This method retrieves the current list of firewall rules and iteratively deletes each rule
        by sending a DELETE request to the API. For each successful deletion, it prints the status
        and additional information returned by the API.

        Raises:
            Any exceptions raised by the underlying API calls are not explicitly handled.

        Note:
            Assumes that `self.get_firewall_rules()` populates `self.firewall_rules` with a list of
            rules, where each rule is an iterable and the first element (`i[0]`) is the rule ID.
            Also assumes the existence of `self.api.api_delete()` and `valid_response_vultr()`.
        """
        if not self.firewall_selected():
            return
        self.get_firewall_rules()
        for i in self.firewall_rules:
            self.firewall_rule_id = i[0]
            self.delete_firewall_rule()

    def delete_firewall_rule_with_notes(self):
        """
        Deletes firewall rules based on user-selected notes.
        This method first checks if a firewall is selected. It then compiles a list of unique notes from the existing firewall rules.
        The user is prompted to select a note from this list. All firewall rules with a note matching the user's selection are deleted.
        Returns:
            None
        """
        if not self.firewall_selected():
            return

        # list all unique firewall rule notes
        notes = []
        for i in self.firewall_rules:
            new_dict = {'name': i[9]}
            if new_dict not in notes:
                notes.append(new_dict)

        # Prompt user to select a firewall rule
        option, fw_list = print_input_menu(notes, 'What firewall to select?: ', 'name', ['name'], False)

        # Delete firewall rules with matching notes
        for i in self.firewall_rules:
            if i[9] == fw_list[int(option) - 1][0]:
                self.firewall_rule_id = i[0]
                self.delete_firewall_rule()

    def delete_firewall_rule(self):
        """
        Deletes a selected firewall rule from the currently selected firewall.
        This method checks if both a firewall and a firewall rule are selected.
        If both are selected, it sends a DELETE request to the API to remove the specified firewall rule.
        Upon a successful response, it prints the status and information returned by the API.
        Returns:
            None
        """
        if not self.firewall_selected():
            return
        if not self.__firewall_rule_selected():
            return
        url = f'firewalls/{self.firewall_id}/rules/{self.firewall_rule_id}'
        data = self.api.api_delete(url)
        if valid_response_vultr(data):
            print(f" {data['status']}: {data['info']}")

    def add_ip4_to_firewall_rules(self):
        """
        Prompts the user for notes and adds the current public IPv4 address to the firewall rules.
        This method retrieves the user's public IPv4 address using the `ipify` service,
        prompts the user to enter notes for the firewall rule (defaulting to 'Added by pyvultr' if left blank),
        and then adds the IP address to the firewall rules with the provided notes.
        Returns:
            None
        """
        if not self.firewall_selected():
            return
        notes = print_text_prompt("Notes for the firewall rules?['Added by pyvultr']: ")
        if notes == '':
            notes = 'Added by pyvultr'
        ip4 = self.ipify.get_ip4()
        print('My public IP4 address is: {}'.format(ip4))
        self.add_ip_to_firewall_rules('v4', ip4, notes)

    def add_ip6_to_firewall_rules(self):
        """
        Prompts the user for notes and adds the current public IPv6 address to the firewall rules.
        This method retrieves the user's public IPv6 address using the `ipify` service,
        prompts the user to enter notes for the firewall rule (defaulting to 'Added by pyvultr' if left blank),
        and then adds the IP address to the firewall rules with the provided notes.
        Returns:
            None
        """
        if not self.firewall_selected():
            return
        notes = print_text_prompt("Notes for the firewall rules?['Added by pyvultr']: ")
        if notes == '':
            notes = 'Added by pyvultr'
        ip6 = self.ipify.get_ip6()
        print('My public IP6 address is: {}'.format(ip6))
        # self.add_ip_to_firewall_rules(ip6_network_prefix(ip6), notes)
        self.add_ip_to_firewall_rules('v6', ip6, notes)

    def add_ip_to_firewall_rules(self, type, ip_address, notes):
        """
        Adds a given IP address to the firewall rules for all supported protocols (TCP, UDP, ICMP).
        Args:
            type (str): The type of IP address (e.g., 'v4' or 'v6').
            ip_address (str): The IP address to add to the firewall rules.
            notes (str): Notes or description for the firewall rule.
        Returns:
            None
        Side Effects:
            - Sends POST requests to the API to add firewall rules for TCP, UDP, and ICMP protocols.
            - Prints a message for each successfully added rule.
            - Displays a table of the added firewall rules.
        Preconditions:
            - A firewall must be selected (self.firewall_selected() returns True).
        """
        if not self.firewall_selected():
            return

        result = []
        params = (
            ('tcp', '1:65535',),
            ('udp', '1:65535',),
            ('icmp', '',),
        )

        url = f'firewalls/{self.firewall_id}/rules'
        for p in params:
            body = {
                    "ip_type": type,
                    "protocol": p[0],
                    "port": p[1],
                    "subnet": ip_address,
                    "subnet_size": 32,
                    "source": "",
                    "notes": notes
                }

            data = self.api.api_post(url, body)
            if valid_response_vultr(data):
                print('Added Firewall Rule')
                detail_row = [
                    data['firewall_rule']['type'],
                    data['firewall_rule']['action'],
                    data['firewall_rule']['protocol'],
                    data['firewall_rule']['subnet'] + '/' + str(data['firewall_rule']['subnet_size']),
                    data['firewall_rule']['port'],
                    data['firewall_rule']['notes'],
                ]
                result.append(detail_row)

        print_output_table(result, self.firewall_rules_header)

    def firewall_selected(self):
        """
        Checks if a firewall has been selected by verifying that `self.firewall_id` is not an empty string.

        Returns:
            bool: True if a firewall is selected (`self.firewall_id` is not empty), False otherwise.
                  Prints a message if no firewall is selected.
        """
        if self.firewall_id != '':
            return True
        else:
            print(yellow_text('No Firewall Selected!'))
            return False

    def __firewall_rule_selected(self):
        """
        Checks if a firewall rule is currently selected.
        Returns:
            bool: True if a firewall rule ID is set (not an empty string), False otherwise.
                  Prints a message if no firewall rule is selected.
        """
        if self.firewall_rule_id != '':
            return True
        else:
            print('No Firewall Rule Selected!')
            return False
