from util import print_input_menu, valid_response_vultr, print_output_table, format_currency
from data import create_data_cache, load_data_cache
import settings

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
    preferred_plan_ids = settings.PREFERRED_PLAN_IDS
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
        Fetches plan data from the API, formats the monthly cost for each plan, and saves the processed data to a cache file.

        This method performs the following steps:
        1. Retrieves plan data from the API endpoint.
        2. Validates the API response.
        3. Formats the 'monthly_cost' field for each plan into a currency string and adds it as 'monthly_cost_str'.
        4. Saves the updated plan data to a cache file.

        Returns:
            None
        """
        url = 'plans'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            for plan in data["plans"]:
                plan["monthly_cost_str"] = format_currency(plan['monthly_cost'])
            print('Saving plans data')
            create_data_cache(self.cache_file, data)

    def print_plan(self):
        """
        Prints the details of the currently selected plan in a formatted table.

        The method checks if a plan is selected, retrieves the selected plan's details,
        and displays its attributes such as ID, vCPU count and type, RAM, disk information,
        bandwidth, monthly cost, type, CPU vendor, and storage type in a tabular format.

        Returns:
            None
        """
        if self.__plan_selected():
            sel_plan = next((plan for plan in self.plans['plans'] if plan['id'] == self.plan_id), None)
            if sel_plan:
                result = [
                    ['ID', sel_plan['id']],
                    ['vCPU Count', sel_plan['vcpu_count']],
                    ['vCPU Type', sel_plan['vcpu_type']],
                    ['RAM', sel_plan['ram']],
                    ['Disk', sel_plan['disk']],
                    ['Disk Count', sel_plan['disk_count']],
                    ['Disk Type', sel_plan['disk_type']],
                    ['Bandwidth', sel_plan['bandwidth']],
                    ['Monthly Cost', sel_plan['monthly_cost_str']],
                    ['Type', sel_plan['type']],
                    ['CPU Vendor', sel_plan['cpu_vendor']],
                    ['Storage Type', sel_plan['storage_type']],
                ]
                print_output_table(result)

    def get_preferred_plans(self):
        """
        Filters and stores the plans whose IDs are listed in `self.preferred_plan_ids`.

        Iterates through the list of preferred plan IDs and searches for matching plans in `self.plans['plans']`.
        Each matching plan is appended to `self.preferred_plans`.

        Returns:
            None
        """
        self.preferred_plans = []
        for o in self.preferred_plan_ids:
            for plan in self.plans['plans']:
                if plan.get("id") == o:
                    self.preferred_plans.append(plan)
                    break

    def get_region_plans(self):
        """
        Filters and stores plans available for the currently selected region.

        Iterates through all available plans and checks if the selected region's ID
        is present in each plan's 'locations'. If so, the plan is added to the
        'region_plans' list. Returns True if a region is selected and plans are filtered,
        otherwise returns False.

        Returns:
            bool: True if a region is selected and plans are filtered, False otherwise.
        """
        if self.obj_region.region_selected():
            self.region_plans = []
            for plan in self.plans['plans']:
                if self.obj_region.region_id in plan.get('locations'):
                    self.region_plans.append(plan)
            return True
        else:
            return False

    def get_preferred_region_plans(self):
        """
        Filters and stores plans available in the currently selected region that match preferred plan IDs.

        Returns:
            bool: True if a region is selected and preferred region plans are updated, False otherwise.

        Side Effects:
            Updates self.preferred_region_plans with plans that are available in the selected region and whose IDs are in self.preferred_plan_ids.
        """
        if self.obj_region.region_selected():
            self.preferred_region_plans = []
            for plan in self.plans['plans']:
                if self.obj_region.region_id in plan.get('locations') and plan.get('id') in self.preferred_plan_ids:
                    self.preferred_region_plans.append(plan)
            return True
        else:
            return False

    def select_all_plans(self, zero_row = True):
        """
        Displays all available plans by printing the list of plans.

        This method retrieves the 'plans' from the instance's `plans` attribute and
        passes them to the internal `__print_plans` method for display.

        Returns:
            None
        """
        self.__print_plans(self.plans['plans'], zero_row)

    def select_preferred_plans(self, zero_row = True):
        """
        Displays the list of preferred plans by printing them.

        This method calls the internal __print_plans function with the preferred_plans attribute,
        which outputs the available preferred plans to the console.

        Returns:
            None
        """
        self.__print_plans(self.preferred_plans, zero_row)

    def select_region_plans(self, zero_row = True):
        """
        Displays the available plans for the selected region.

        This method checks if there are any plans available for the current region
        by calling `get_region_plans()`. If plans are available, it prints them
        using the `__print_plans` method.

        Returns:
            None
        """
        if self.get_region_plans():
            self.__print_plans(self.region_plans, zero_row)

    def select_preferred_region_plans(self, zero_row = True):
        """
        Selects and prints the plans available in the preferred region.

        This method checks if there are any preferred region plans available by calling
        `get_preferred_region_plans()`. If plans are found, it prints them using the
        `__print_plans` method.

        Returns:
            None
        """
        if self.get_preferred_region_plans():
            self.__print_plans(self.preferred_region_plans, zero_row)

    def __print_plans(self, plan_set, zero_row):
        """
        Prints all available plans in a formatted table.

        Utilizes the `print_output_table` function to display the plans stored in `self.plans['plans']`.
        Returns:
            None
        """
        display_row = ['id', 'ram', 'disk', 'vcpu_count', 'bandwidth', 'monthly_cost_str', 'type']
        header_row = ['Sel', 'Name', 'RAM', 'Disk Size', 'vCPU Count', 'Bandwidth', 'Monthly Cost', 'Type']
        offset = 1
        if zero_row:
            offset = 0
        option, r_list = print_input_menu(plan_set, 'What plan to select?: ', 'id', display_row, zero_row, header_row)
        self.plan_id = r_list[int(option) - offset][0]
        self.plan_desc = r_list[int(option) - offset][1]

    def __plan_selected(self):
        """
        Checks if a plan has been selected by verifying that `plan_id` is not an empty string.

        Returns:
            bool: True if a plan is selected (`plan_id` is not empty), False otherwise.
            Prints a message if no plan is selected.
        """
        if self.plan_id != '':
            return True
        else:
            print('No Plan Selected!')
            return False
