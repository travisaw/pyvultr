from util import utc_to_local

def get_firewalls(api):
    url = 'firewalls'
    data = api.api_get(url)
    # print(data)
    fw_list = []
    fw_count = 1
    for i in data['firewall_groups']:
        # print(i)
        if fw_count == 1:
            print('0. None')
        inst = [i['id'], i['description']]
        fw_list.append(inst)
        print(str(fw_count) + '. '+ i['description'])
        fw_count += 1
    option = input("What firewall to select?: ")
    # print('Name: ', data['account']['name'])
    # print('Email: ', data['account']['email'])
    # print('Balance: ', data['account']['balance'])
    # print('Pending Charges: ', data['account']['pending_charges'])
    # print('Last Payment Date: ', utc_to_local(data['account']['last_payment_date']))
    # print('Last Payment Amount: ', data['account']['last_payment_amount'])

def get_firewall(api):
    pass

def create_firewall(api, description):
    pass
