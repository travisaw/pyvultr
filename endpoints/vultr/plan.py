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
        self.cache_file = 'vultr_plans.json'
        self.plans = self.load_plans()
        self.obj_region = region

    def load_plans(self):
        """
        Loads plans from the cache file if it exists, otherwise retrieves them from the API.

        Returns:
            A list of plans loaded from the cache or API.
        """
        data = load_data_cache(self.cache_file)
        if data is None:
            print('No cached plans found, retrieving from API.')
            self.save_plans()
            data = load_data_cache(self.cache_file)
        return data

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

    def get_all_plan(self):
        """
        Displays a menu of available plans for selection and sets the selected plan's ID and description.

        Uses the `print_input_menu` function to present the user with a list of plans and prompts for a selection.
        Updates `self.plan_id` and `self.plan_desc` with the ID and description of the chosen plan.

        Returns:
            None
        """
        option, r_list = print_input_menu(self.plans['plans'], 'What plan to select?: ', 'id', ['id', 'ram', 'disk', 'vcpu_count', 'bandwidth', 'monthly_cost', 'type'], False)
        self.plan_id = r_list[int(option) - 1][0]
        self.plan_desc = r_list[int(option) - 1][1]

    def get_preferred_plan(self):
        """
        Selects a preferred plan from a predefined list of options.

        This method filters available plans to match specific IDs ('vc2-1c-1gb', 'vc2-1c-2gb'),
        presents them to the user via an input menu, and sets the selected plan's ID and description
        as instance attributes.

        Returns:
            None

        Side Effects:
            Sets self.plan_id and self.plan_desc based on user selection.
        """
        options = ['vc2-1c-1gb', 'vc2-1c-2gb']
        plans = []
        for o in options:
            for plan in self.plans['plans']:
                if plan.get("id") == o:
                    plans.append(plan)
                    break
        option, r_list = print_input_menu(plans, 'What plan to select?: ', 'id', ['id', 'ram', 'disk', 'vcpu_count', 'bandwidth', 'monthly_cost', 'type'], False)
        self.plan_id = r_list[int(option) - 1][0]
        self.plan_desc = r_list[int(option) - 1][1]

    def get_region_plan(self):
        pass
