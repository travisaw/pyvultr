from util import print_input_menu, print_output_table, valid_response_vultr
from data import create_data_cache, load_data_cache
import settings

class Application:
    application_id = str('')
    application_desc = str('')
    application_image_id = str('')
    preferred_application_ids = settings.PREFERRED_APPLICATION_IDS

    def __init__(self, api):
        self.api = api
        self.cache_file = 'vultr_applications.json'
        self.applications = self.load_applications()

    def load_applications(self):
        data = load_data_cache(self.cache_file)
        if data is None:
            print('No cached applications found, retrieving from API.')
            self.save_applications()
            data = load_data_cache(self.cache_file)
        return data

    def save_applications(self):
        url = 'applications'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            print('Saving application data')
            create_data_cache(self.cache_file, data)
            self.load_applications()

    def print_application(self):
        if self.__application_selected():
            sel_application = next((application for application in self.applications['applications'] if application['id'] == self.application_id), None)
            if sel_application:
                print(sel_application)
                data = [
                    ['ID', sel_application['id']],
                    ['Name', sel_application['name']],
                    ['Short Name', sel_application['short_name']],
                    ['Deploy Name', sel_application['deploy_name']],
                    ['Type', sel_application['type']],
                    ['Vendor', sel_application['vendor']],
                    ['Image Id', sel_application['image_id']],
                ]
                print_output_table(data)

    def get_all_applications(self):
        option, r_list = print_input_menu(self.applications['applications'], 'What Application to select?: ', 'id', ['id', 'name', 'type'], True)
        self.application_id = r_list[int(option) - 1][0]
        app = next((app for app in self.applications['applications'] if app['id'] == self.application_id), None)
        self.application_desc = app['name']
        self.application_image_id = app['image_id']

    def get_preferred_applications(self):
        applications_out = []
        for a in self.preferred_application_ids:
            for app in self.applications['applications']:
                if app.get('id') == a:
                    applications_out.append(app)
                    break
        option, r_list = print_input_menu(applications_out, 'What Application to select?: ', 'id', ['id', 'name', 'type'], False)

        self.application_id = r_list[int(option) - 1][0]
        app = next((app for app in self.applications['applications'] if app['id'] == self.application_id), None)
        self.application_desc = app['name']
        self.application_image_id = app['image_id']

    def __application_selected(self):
        if self.application_id != '':
            return True
        else:
            print('No Application Selected!')
            return False
