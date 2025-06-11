from util import utc_to_local, print_input_menu, valid_response_cloudflare
from tabulate import tabulate

class Zone:
    """
    Zone
    A class to interact with Cloudflare DNS zones and records via an API.
    Attributes:
        zone_id (str): ID of the selected DNS zone.
        zone_detail (dict): Details of the selected DNS zone.
        dns_records (dict): All DNS records in the selected zone.
        dns_records_header (list): Header used when printing DNS records.
        dns_record_id (str): ID of the selected DNS record.
        dns_record (dict): Details of the selected DNS record.
        api: API client instance for making requests.
    Methods:
        __init__(api):
            Initialize the Zone object with an API client.
        verify_token():
            Verify the API token. (Note: This method may not belong in this class.)
        get_zones():
            Retrieve all available zones (domains) accessible to the token and prompt user to select one.
        get_zone():
            Load details of the selected zone into local variables.
        print_zone():
            Print details of the currently selected zone.
        get_dns_records():
            Load DNS records of the selected zone into a local variable.
        print_dns_records():
            Print a list of DNS entries for the selected zone.
        get_dns_record_of_type(type):
            Print a list of DNS records filtered by type and prompt user to select one.
        get_dns_record_by_name_content(name, content):
            Load DNS record ID by matching its name and content.
        print_dns_record():
            Print details of the currently selected DNS record.
        create_dns_record_prompt():
            Prompt the user for DNS record details and create the record.
        create_dns_record(body):
            Create a DNS record using the provided details.
        delete_dns_record():
            Delete the currently selected DNS record.
        __zone_selected():
            Check if a DNS zone is selected and DNS records are loaded.
    """
    zone_id = str('')   # ID of select DNS zone
    zone_detail = {}    # Dictionary containing details of DNS Zone
    dns_records = {}    # Dictionary containing all DNS records in selected zone
    dns_records_header = ['Name', ' Type', 'Content', 'Proxied'] # Header used when printing list of DNS records in zone
    dns_record_id = str('') # ID of selected DNS record
    dns_record = {}     # Dictionary containing details of selected DNS record

    def __init__(self, api):
        """
        Initialize the class with the provided API client.

        Args:
            api: An instance of the API client to be used for making requests.
        """
        self.api = api

    def verify_token(self):
        """
        Verifies the API token by making a request to the token verification endpoint.

        Returns:
            None

        Side Effects:
            Prints a formatted table displaying the status, success flag, errors, message, and message code
            from the API token verification response.

        Note:
            This method prints the result to the console and does not return any value.
        """
        url = 'user/tokens/verify'
        data = self.api.api_get(url)
        result = [
            ['Status: ', data['result']['status']],
            ['Success: ', data['success']],
            ['Errors: ', data['errors']],
            ['Message: ', data['messages'][0]['message']],
            ['Message Code: ', data['messages'][0]['code']],
        ]
        print(tabulate(result))

    def get_zones(self):
        """
        Retrieves all available Cloudflare zones (domains) accessible with the current API token.

        Presents the user with a menu to select a zone, then sets the selected zone's ID,
        fetches its details, and retrieves its DNS records.

        Returns:
            None

        Side Effects:
            - Updates self.zone_id with the selected zone's ID.
            - Calls self.get_zone() to fetch details of the selected zone.
            - Calls self.get_dns_records() to retrieve DNS records for the selected zone.
        """
        url = 'zones'
        data = self.api.api_get(url)
        if valid_response_cloudflare(data):
            option, inst_list = print_input_menu(data['result'], 'What zone to select?: ', 'id', ['name'], True)
            self.zone_id = inst_list[int(option)][0]
            self.get_zone()
            self.get_dns_records()

    def get_zone(self):
        """
        Fetches and loads the details of the currently selected Cloudflare zone.

        If a zone ID is set, retrieves the zone details from the Cloudflare API and stores them in `self.zone_detail`
        if the response is valid. If no zone ID is set, clears `self.zone_detail`.

        Returns:
            None
        """
        if self.zone_id != '':
            url = f'zones/{self.zone_id}'
            data = self.api.api_get(url)
            if valid_response_cloudflare(data):
                self.zone_detail = data['result']
        else:
            self.zone_detail = {}

    def print_zone(self):
        """
        Prints the details of the currently selected DNS zone in a tabular format.

        If a zone is selected (i.e., 'name' exists in self.zone_detail), this method displays key information
        such as the zone's name, status, paused state, name servers, original registrar, and important dates
        (created, activated, and updated), converting UTC timestamps to local time. If no zone is selected,
        it prints a message indicating that no DNS zone is selected.
        """
        if 'name' in self.zone_detail:
            result = [
                ['Name: ', self.zone_detail['name']],
                ['Status: ', self.zone_detail['status']],
                ['Paused: ', self.zone_detail['paused']],
                ['Name Servers: ', self.zone_detail['name_servers']],
                ['Original Registrar: ', self.zone_detail['original_registrar']],
                ['Date Created: ', utc_to_local(self.zone_detail['created_on'])],
                ['Date Activated: ', utc_to_local(self.zone_detail['activated_on'])],
                ['Date Updated: ', utc_to_local(self.zone_detail['modified_on'])],
            ]
            print(tabulate(result))
        else:
            print("No DNS Zone Selected!")

    def get_dns_records(self):
        """
        Fetches and loads the DNS records for the currently selected zone.

        If a valid zone ID is set, retrieves DNS records from the API and stores them in the `dns_records` attribute.
        If no zone ID is set, initializes `dns_records` as an empty dictionary.
        """
        if self.zone_id != '':
            url = f'zones/{self.zone_id}/dns_records'
            data = self.api.api_get(url)
            self.dns_records = data['result']
        else:
            self.dns_records = {}

    def print_dns_records(self):
        """
        Prints a formatted table of DNS records for the selected zone.

        This method checks if a zone is currently selected. If so, it iterates over the DNS records associated with the zone,
        extracting the name, type, a truncated version of the content (up to 40 characters), and the proxied status for each record.
        The records are then displayed in a tabular format using the headers defined in `self.dns_records_header`.

        Returns:
            None
        """
        if self.__zone_selected():
            result = []
            for i in self.dns_records:
                row = [
                    i['name'],
                    i['type'],
                    i['content'][:40],
                    i['proxied'],
                ]
                result.append(row)
            print(tabulate(result, self.dns_records_header))

    def get_dns_record_of_type(self, type):
        """
        Displays a list of DNS records filtered by the specified type(s) and prompts the user to select one.

        Args:
            type (str or list): The DNS record type(s) to filter by. If an empty string is provided, all types are displayed.
                                If a list is provided, only records matching any type in the list are shown.

        Returns:
            None: The method sets the selected DNS record's ID to `self.dns_record_id` based on user input.

        Side Effects:
            Prompts the user to select a DNS record from the filtered list.
            Updates `self.dns_record_id` with the ID of the selected DNS record.

        Note:
            Requires that a zone is selected (`self.__zone_selected()` returns True).
        """
        if self.__zone_selected():
            result = []
            for i in self.dns_records:
                if i['type'] in type or type == '':
                    result.append({'id': i['id'], 'name': i['name'], 'type': i['type'], 'content': i['content']})
            option, dns_list = print_input_menu(result, 'What entry to select?: ', 'id', ['name', 'type', 'content'], True)
            self.dns_record_id = dns_list[int(option)][0]

    def get_dns_record_by_name_content(self, name, content):
        """
        Retrieve and store the DNS record ID for a DNS record matching the given name and content.

        Args:
            name (str): The subdomain or record name (without the zone suffix) to search for.
            content (str): The content value of the DNS record to match (e.g., IP address or target).

        Returns:
            bool: True if a matching DNS record is found and its ID is stored; False otherwise.

        Side Effects:
            Sets self.dns_record_id to the ID of the found DNS record if a match is found.
        """
        full_name = name + '.' + self.zone_detail['name']
        for i in self.dns_records:
            if i['name'] == full_name and i['content'] == content:
                print('Found DNS Record.')
                self.dns_record_id = i['id']
                return True
        print('No DNS Record Found.')
        return False

    def print_dns_record(self):
        """
        Prints the details of the currently selected DNS record in a tabular format.

        If a DNS record is selected (i.e., `self.dns_record_id` is set), this method searches for the corresponding DNS record
        in `self.dns_records` and displays its attributes such as name, type, content, proxy status, TTL, settings, metadata,
        comments, tags, and timestamps (converted to local time) using the `tabulate` library. If no DNS record is selected,
        it prints a message indicating that no DNS record is selected.
        """
        if self.dns_record_id:
            match = next((d for d in self.dns_records if d.get('id') == self.dns_record_id), None)
            result = [
                ['Name: ', match['name']],
                ['Type: ', match['type']],
                ['Content: ', match['content']],
                ['Proxiable: ', match['proxiable']],
                ['Proxied: ', match['proxied']],
                ['TTL: ', match['ttl']],
                ['Settings: ', match['settings']],
                ['Meta: ', match['meta']],
                ['Comment: ', match['comment']],
                ['Tags: ', match['tags']],
                ['Created On: ', utc_to_local(match['created_on'])],
                ['Modified On: ', utc_to_local(match['modified_on'])],
            ]
            print(tabulate(result))
        else:
            print('No DNS Record Selected')

    def create_dns_record_prompt(self):
        """
        Prompts the user to enter details for a new DNS record (name and IP address), constructs the DNS record data,
        and passes it to the method responsible for creating the DNS record.

        The DNS record is created with the following default properties:
        - Comment: "Added by pyvultr"
        - Proxied: True
        - TTL: 300 seconds
        - Type: "A"

        Calls:
            self.create_dns_record(body): Creates the DNS record with the specified details.
        """
        name = input('DNS Name:')
        content = input('IP Address:')
        body = {
            "comment": "Added by pyvultr",
            "content": content,
            "name": name,
            "proxied": True,
            "ttl": 300,
            "type": "A"
        }
        self.create_dns_record(body)

    def create_dns_record(self, body):
        """
        Creates a DNS record in the specified Cloudflare zone using the provided details.

        Args:
            body (dict): A dictionary containing the DNS record details required by the Cloudflare API.

        Returns:
            None

        Side Effects:
            - Sends a POST request to the Cloudflare API to create a DNS record.
            - Calls `get_zone()` to refresh the zone information if the record is created successfully.
            - Prints a message indicating the DNS entry was created and needs to be selected.

        Raises:
            Any exceptions raised by the underlying API call are not explicitly handled here.
        """
        url = f'zones/{self.zone_id}/dns_records'
        data = self.api.api_post(url, body)
        if valid_response_cloudflare(data):
            self.get_zone()
            print('DNS entry created. Record will need to be selected.')

    def delete_dns_record(self):
        """
        Deletes a DNS record from Cloudflare using the API.

        This method constructs the appropriate API endpoint URL using the zone ID and DNS record ID,
        then sends a DELETE request via the API client. If the response is valid and indicates success,
        a confirmation message is printed.

        Returns:
            None
        """
        # if 'prod' in self.instance_tags:
        #     print(f"CANNOT DELETE PRODUCTION INSTANCE")
        #     return
        url = f'zones/{self.zone_id}/dns_records/{self.dns_record_id}'
        data = self.api.api_delete(url)
        if valid_response_cloudflare(data):
            print(f"Success: {data['success']} - Record deleted.")

    def __zone_selected(self):
        """
        Checks if a DNS zone is selected by verifying the presence of DNS records.

        Returns:
            bool: True if DNS records exist (zone is selected), False otherwise. Prints a message if no zone is selected.
        """
        if self.dns_records:
            return True
        else:
            print('No DNS Zone Selected!')
            return False
