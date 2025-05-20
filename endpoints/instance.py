from util import utc_to_local, valid_option, ip6_network_prefix

class Instance:
    instance_id = str('')

    def __init__(self, api):
        self.api = api
            
    def get_instances(self):
        url = 'instances'
        data = self.api.api_get(url)
        inst_list = []
        inst_count = 1
        for i in data['instances']:
            if inst_count == 1:
                print('0. None')
            inst = [i['id'], i['label']]
            inst_list.append(inst)
            print(str(inst_count) + '. '+ i['label'])
            inst_count += 1
        option = input("What instance to select?: ")
        # if not valid_option(option, inst_list):
        #     print("Invalid Option")
        #     return
        self.instance_id = inst_list[int(option) - 1][0]

    def get_instance(self):
        print('Yeah!')
        url = f'instances/{self.instance_id}'
        data = self.api.api_get(url)
        print(data)
        # print('Name: ', data['account']['name'])
        # print('Email: ', data['account']['email'])
        # print('Balance: ', data['account']['balance'])
        # print('Pending Charges: ', data['account']['pending_charges'])
        # print('Last Payment Date: ', utc_to_local(data['account']['last_payment_date']))
        # print('Last Payment Amount: ', data['account']['last_payment_amount'])
