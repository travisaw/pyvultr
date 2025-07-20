from util import print_input_menu, valid_response_vultr, print_output_table
from data import create_data_cache, load_data_cache

class Plan:
    """
    Plan class for managing and selecting Vultr server plans.
        plan_id (str): The ID of the selected plan.
        plan_desc (str): The description of the selected plan.
        api: Instance of the API client used for making requests.
        cache_file (str): The filename used for caching plan data.
        plans (list): List of plans loaded from the cache or API.
        obj_region: The region object associated with the plan.
    Methods:
        __init__(api, region):
            Initializes the Plan class with the provided API client and region, sets up caching, and loads available plans.
        load_plans():
            Loads plans from the cache file if available, otherwise retrieves them from the API and caches them.
        save_plans():
            Retrieves plan data from the Vultr API and saves it to the cache file.
        get_all_plan():
            Displays a menu of all available plans for user selection and sets the selected plan's ID and description.
        get_preferred_plan():
            Filters available plans to a predefined list of preferred options, presents them for selection, and sets the selected plan's ID and description.
        get_region_plan():
            Placeholder for future implementation to select plans based on region.
    """
    plan_id = str('')
    plan_desc = str('')
    preferred_plan_ids = ['vc2-1c-1gb', 'vc2-1c-2gb', 'vc2-1c-0.5gb-v6']
    plans = {}
    preferred_plans = []
    region_plans = []
    preferred_region_plans = []

    def __init__(self, api, region):
        """
        Initializes the Plan class with the provided API client, sets the cache file name, and loads available plans.
            api: An instance of the API client used for making requests.
        Attributes:
            api: Stores the provided API client instance.
            cache_file: The filename used for caching plan data.
            plans: A list of plans loaded from the cache or API.
        """
        self.api = api
        self.obj_region = region
        self.cache_file = 'vultr_plans.json'
        self.load_plans()
        self.get_preferred_plans()

    def load_plans(self):
        """
        Loads plan data from the cache file into the `self.plans` attribute.

        If the cache file does not exist or contains no data, retrieves the plans from the API,
        saves them to the cache, and reloads the plans from the cache file.

        Side Effects:
            - Updates `self.plans` with the loaded or retrieved plan data.
            - May print a message if no cached plans are found.
            - May call `self.save_plans()` to fetch and cache plans from the API.
        """
        self.plans = {}
        self.plans = load_data_cache(self.cache_file)
        if self.plans is None:
            print('No cached plans found, retrieving from API.')
            self.save_plans()
            self.plans = load_data_cache(self.cache_file)

    def save_plans(self):
        """
        Retrieves plan data from the Vultr API and saves it to a cache file.
        This method sends a GET request to the 'plans' endpoint using the API client.
        If the response is valid, it prints a message and caches the data locally.
        Returns:
            None
        """
        url = 'plans'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            print('Saving plans data')
            create_data_cache(self.cache_file, data)

    def get_preferred_plans(self):
        self.preferred_plans = []
        for o in self.preferred_plan_ids:
            for plan in self.plans['plans']:
                if plan.get("id") == o:
                    self.preferred_plans.append(plan)
                    break

    def get_region_plans(self):
        if self.obj_region.region_selected():
            self.region_plans = []
            for plan in self.plans['plans']:
                if self.obj_region.region_id in plan.get('locations'):
                    self.region_plans.append(plan)
            return True
        else:
            return False
        
    def get_preferred_region_plans(self):
        pass

    def select_all_plans(self):
        option, r_list = print_input_menu(self.plans['plans'], 'What plan to select?: ', 'id', ['id', 'ram', 'disk', 'vcpu_count', 'bandwidth', 'monthly_cost', 'type'], True)
        self.plan_id = r_list[int(option) - 1][0]
        self.plan_desc = r_list[int(option) - 1][1]

    def select_preferred_plans(self):
        option, r_list = print_input_menu(self.preferred_plans, 'What plan to select?: ', 'id', ['id', 'ram', 'disk', 'vcpu_count', 'bandwidth', 'monthly_cost', 'type'], True)
        self.plan_id = r_list[int(option) - 1][0]
        self.plan_desc = r_list[int(option) - 1][1]

    def select_region_plans(self):
        if self.get_region_plans():
            option, r_list = print_input_menu(self.region_plans, 'What plan to select?: ', 'id', ['id', 'ram', 'disk', 'vcpu_count', 'bandwidth', 'monthly_cost', 'type'], True)
            self.plan_id = r_list[int(option) - 1][0]
            self.plan_desc = r_list[int(option) - 1][1]

    def select_preferred_region_plans(self):
        pass
