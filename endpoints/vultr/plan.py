from util import print_input_menu, valid_response_vultr

class Plan:
    """
    Plan
    A class to interact with the Vultr Plan API, providing methods to list available plans and prompt the user for selection.
    Methods
    -------
    __init__(api):
        Initializes the Plan instance with the provided API client.
    get_plans():
        Retrieves all available plans from the Vultr API, displays them to the user, and prompts for selection.
    get_preferred_plan():
        Returns a hardcoded list of 'preferred' plans and prompts the user for selection.
    """

    def __init__(self, api):
        """
        Initialize the class with the given API client.

        Args:
            api: An instance of the API client to be used for making requests.
        """
        self.api = api

    def get_plans(self):
        """
        Retrieves a list of available plans from the API, displays them to the user, and prompts for a selection.

        Upon successful retrieval and selection, sets the selected plan's ID and description as instance attributes.

        Returns:
            None

        Raises:
            Any exceptions raised by the API call or user input handling are propagated.
        """
        url = 'plans'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            option, p_list = print_input_menu(data['plans'], 'What plan to select?: ', 'id', ['description'], True)
            self.plan_id = p_list[int(option) - 1][0]
            self.plan_desc = p_list[int(option) - 1][1]

    def get_preferred_plan(self):
        """
        Returns a list of preferred plans.
        This method provides a hardcoded list of 'preferred' plans for the user to select from.
        Currently, the list is empty and should be populated with plan identifiers or objects
        that represent the preferred options.
        Returns:
            list: A list of preferred plan identifiers or objects.
        """
        """List 'preferred' plans and prompt user to select one. List hardcoded."""
        return [

        ]
