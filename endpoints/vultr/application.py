from util import print_input_menu, print_output_table, valid_response_vultr, yellow_text
from data import create_data_cache, load_data_cache
import settings

class Application:
    """
    Manages Vultr one-click application selection and data caching.

    Provides methods to load, save, display, and select applications from
    the Vultr API or a local JSON cache. Selected application state is stored
    as instance attributes.

    Class Attributes:
        application_id (str): The ID of the currently selected application.
        application_desc (str): The name/description of the currently selected application.
        application_image_id (str): The image ID of the currently selected application.
        preferred_application_ids (list): Application IDs from settings to use as a filtered list.
    """
    application_id = str('')
    application_desc = str('')
    application_image_id = str('')
    preferred_application_ids = settings.PREFERRED_APPLICATION_IDS

    def __init__(self, api):
        """
        Initializes the Application instance and loads application data from cache.

        Args:
            api: An authenticated Vultr API client used for HTTP requests.
        """
        self.api = api
        self.cache_file = 'vultr_applications.json'
        self.applications = self.load_applications()

    def load_applications(self):
        """
        Loads application data from the local JSON cache.

        If no cached data exists, fetches and saves it from the Vultr API first.

        Returns:
            dict: The applications data, structured as returned by the Vultr API.
        """
        data = load_data_cache(self.cache_file)
        if data is None:
            print('No cached applications found, retrieving from API.')
            self.save_applications()
            data = load_data_cache(self.cache_file)
        return data

    def save_applications(self):
        """
        Fetches application data from the Vultr API and saves it to the local cache.

        Validates the API response before writing. Reloads the in-memory applications
        data after saving.

        Returns:
            None
        """
        url = 'applications'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            print('Saving application data')
            create_data_cache(self.cache_file, data)
            self.load_applications()

    def print_application(self):
        """
        Prints a formatted table of details for the currently selected application.

        Displays fields including ID, name, short name, deploy name, type, vendor,
        and image ID. Does nothing if no application is currently selected.

        Returns:
            None
        """
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
        """
        Presents an interactive menu of all available applications and sets the selected application.

        Prompts the user to choose from the full application list. Updates
        application_id, application_desc, and application_image_id with the selection.

        Returns:
            None
        """
        option, r_list = print_input_menu(self.applications['applications'], 'What Application to select?: ', 'id', ['id', 'name', 'type'], True)
        self.application_id = r_list[int(option) - 1][0]
        app = next((app for app in self.applications['applications'] if app['id'] == self.application_id), None)
        self.application_desc = app['name']
        self.application_image_id = app['image_id']

    def get_preferred_applications(self):
        """
        Presents an interactive menu filtered to preferred application IDs and sets the selected application.

        Filters the full application list to only those whose IDs appear in
        settings.PREFERRED_APPLICATION_IDS. Updates application_id, application_desc,
        and application_image_id with the user's selection.

        Returns:
            None
        """
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
        """
        Checks whether an application is currently selected.

        Returns:
            bool: True if an application is selected (application_id is non-empty), False otherwise.
                  Prints a warning message if no application is selected.
        """
        if self.application_id != '':
            return True
        else:
            print(yellow_text('No Application Selected!'))
            return False
