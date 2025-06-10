from util import utc_to_local, print_input_menu, valid_response_cloudflare
from tabulate import tabulate

class Zone:
    """Contains methods for interacting with the Cloudflare DNS Zones API."""
    zone_id = str('')   # ID of select DNS zone
    zone_detail = {}    # Dictionary containing details of DNS Zone
    dns_records = {}    # Dictionary containing all DNS records in selected zone
    dns_records_header = ['Name', ' Type', 'Content', 'Proxied'] # Header used when printing list of DNS records in zone
    dns_record_id = str('') # ID of selected DNS record
    dns_record = {}     # Dictionary containing details of selected DNS record

    def __init__(self, api):
        self.api = api

    def verify_token(self):
        """Verify API token (technically doesn't below in this class)."""
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
        """Get all available zones (domains) available to token. User can select zone to use used for other operations."""
        url = 'zones'
        data = self.api.api_get(url)
        if valid_response_cloudflare(data):
            option, inst_list = print_input_menu(data['result'], 'What zone to select?: ', 'id', ['name'], True)
            self.zone_id = inst_list[int(option)][0]
            self.get_zone()
            self.get_dns_records()

    def get_zone(self):
        """Load details of selected zone into local variables."""
        if self.zone_id != '':
            url = f'zones/{self.zone_id}'
            data = self.api.api_get(url)
            if valid_response_cloudflare(data):
                self.zone_detail = data['result']
        else:
            self.zone_detail = {}

    def print_zone(self):
        """Print details of selected zone."""
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
        """Load DNS records of selected zone into local variable."""
        if self.zone_id != '':
            url = f'zones/{self.zone_id}/dns_records'
            data = self.api.api_get(url)
            self.dns_records = data['result']
        else:
            self.dns_records = {}

    def print_dns_records(self):
        """Print details list of DNS entries for zone."""
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
        Given a list of DNS record types print list of available records for user to select. 
        If no type is given all types will be displayed.
        """
        if self.__zone_selected():
            result = []
            for i in self.dns_records:
                if i['type'] in type or type == '':
                    result.append({'id': i['id'], 'name': i['name'], 'type': i['type'], 'content': i['content']})
            option, dns_list = print_input_menu(result, 'What entry to select?: ', 'id', ['name', 'type', 'content'], True)
            self.dns_record_id = dns_list[int(option)][0]

    def get_dns_record_by_name_content(self, name, content):
        """Load DNS record ID given it's name and content."""
        full_name = name + '.' + self.zone_detail['name']
        for i in self.dns_records:
            if i['name'] == full_name and i['content'] == content:
                print('Found DNS Record.')
                self.dns_record_id = i['id']
                return True
        print('No DNS Record Found.')
        return False

    def print_dns_record(self):
        """Print details of selected DNS record."""
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
        """Prompt user for details of DNS record. Pass details to method which creates the DNS record."""
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
        """Calls Cloudfare API to create DNS record with details provided in body."""
        url = f'zones/{self.zone_id}/dns_records'
        data = self.api.api_post(url, body)
        if valid_response_cloudflare(data):
            self.get_zone()
            print('DNS entry created. Record will need to be selected.')

    def delete_dns_record(self):
        """Calls Cloudfare API to delete DNS record."""
        # if 'prod' in self.instance_tags:
        #     print(f"CANNOT DELETE PRODUCTION INSTANCE")
        #     return
        url = f'zones/{self.zone_id}/dns_records/{self.dns_record_id}'
        data = self.api.api_delete(url)
        if valid_response_cloudflare(data):
            print(f"Success: {data['success']} - Record deleted.")

    def __zone_selected(self):
        if self.dns_records:
            return True
        else:
            print('No DNS Zone Selected!')
            return False
