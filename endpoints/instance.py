from util import utc_to_local

def get_instances(api):
    url = 'instances'
    data = api.api_get(url)
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

def get_instance_details(api):
    print('Yeah!')
    # print('Name: ', data['account']['name'])
    # print('Email: ', data['account']['email'])
    # print('Balance: ', data['account']['balance'])
    # print('Pending Charges: ', data['account']['pending_charges'])
    # print('Last Payment Date: ', utc_to_local(data['account']['last_payment_date']))
    # print('Last Payment Amount: ', data['account']['last_payment_amount'])
