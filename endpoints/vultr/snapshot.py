from util import utc_str_to_local, print_input_menu, valid_response_vultr, format_bytes, print_output_table, \
    green_text, yellow_text, red_text

class Snapshot:
    """
    Snapshot
    A class to interact with the Vultr Snapshot API, providing methods to list, retrieve, create, delete, and update snapshots.
    Attributes:
        snapshot_id (str): The ID of the currently selected snapshot.
        snapshot_desc (str): The description of the currently selected snapshot.
        api: An API client instance used to make requests to the Vultr API.
    Methods:
        __init__(api):
            Initializes the Snapshot class with the provided API client.
        get_snapshots():
            Lists all available snapshots and prompts the user to select one. Sets the selected snapshot's ID and description.
        get_snapshot():
            Displays details of the currently selected snapshot.
        create_snapshot(ss_name, instance_id):
            Creates a new snapshot with the given name/description for the specified instance ID.
        delete_snapshot():
            Deletes the currently selected snapshot.
        update_snapshot(ss_name):
            Updates the description of the currently selected snapshot.
        __snapshot_status_color(status):
            Returns a colored string representation of the snapshot status for display purposes.
    """
    snapshot_id = str('')
    snapshot_desc = str('')

    def __init__(self, api):
        """
        Initialize the class with the provided API client.

        Args:
            api: An instance of the API client to be used for making requests.
        """
        self.api = api

    def get_snapshots(self):
        """
        Retrieves all available snapshots from the Vultr API, displays them in a menu for user selection,
        and stores the selected snapshot's ID and description as instance attributes.

        Returns:
            None

        Side Effects:
            Prompts the user to select a snapshot from the list.
            Sets self.snapshot_id and self.snapshot_desc based on the user's selection.
        """
        url = 'snapshots'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            option, ss_list = print_input_menu(data['snapshots'], 'What snapshot to select?: ', 'id', ['description', 'status'], True)
            self.snapshot_id = ss_list[int(option)][0]
            self.snapshot_desc = ss_list[int(option)][1]

    def get_snapshot(self):
        """
        Prints details of the currently selected snapshot.

        If a snapshot is selected (i.e., self.snapshot_id is not empty), this method retrieves the snapshot details from the API,
        formats relevant fields (such as creation date, description, size, compressed size, and status), and prints them in a tabular format.
        If no snapshot is selected, it prints a warning message.

        Returns:
            None
        """
        if self.snapshot_selected():
            url = f'snapshots/{self.snapshot_id}'
            data = self.api.api_get(url)
            if valid_response_vultr(data):
                result = [
                    # ['id', data['snapshot']['id']],
                    ['date_created', utc_str_to_local(data['snapshot']['date_created'])],
                    ['description', data['snapshot']['description']],
                    ['size', format_bytes(data['snapshot']['size'])],
                    ['compressed_size', format_bytes(data['snapshot']['compressed_size'])],
                    ['status', self.__snapshot_status_color(data['snapshot']['status'])],
                ]
                print_output_table(result)

    def create_snapshot(self, ss_name, instance_id):
        """
        Creates a snapshot of a specified instance with a given name or description.

        Args:
            ss_name (str): The name or description for the snapshot.
            instance_id (str): The unique identifier of the instance to snapshot.

        Returns:
            None

        Side Effects:
            Prints a confirmation message if the snapshot is created successfully.
        """
        url = 'snapshots'
        body = {
            "instance_id": instance_id,
            "description": ss_name,
        }
        data = self.api.api_post(url, body)
        if valid_response_vultr(data):
            print(f" Created snapshot '{data['snapshot']['description']}'")

    def delete_snapshot(self):
        """
        Deletes the snapshot associated with the current instance.

        Sends a DELETE request to the Vultr API to remove the snapshot identified by the Snapshot Id`.
        If the response is valid, prints the status and additional information returned by the API.

        Raises:
            Any exceptions raised by the underlying API call or response validation.
        """
        if self.snapshot_selected():
            url = f'snapshots/{self.snapshot_id}'
            data = self.api.api_delete(url)
            if valid_response_vultr(data):
                print(f" {data['status']}: {data['info']}")

    def update_snapshot(self, ss_name):
        """
        Updates the description of the currently selected snapshot.

        Args:
            ss_name (str): The new description for the snapshot.

        Returns:
            None

        Side Effects:
            Sends a PUT request to the Vultr API to update the snapshot's description.
            Prints the status and info from the API response if the response is valid.
        """
        if self.snapshot_selected():
            url = f'snapshots/{self.snapshot_id}'
            body = {
                "description": ss_name,
            }
            data = self.api.api_put(url, body)
            if valid_response_vultr(data):
                print(f" {data['status']}: {data['info']}")

    def snapshot_selected(self):
        """
        Checks whether a snapshot is currently selected.

        Returns:
            bool: True if a snapshot is selected, False otherwise.

        Side Effects:
            Prints a warning message if no snapshot is selected.
        """
        if self.snapshot_id != '':
            return True
        else:
            print(yellow_text('No Snapshot Selected!'))
            return False

    def __snapshot_status_color(self, status):
        """
        Returns the status string colored according to its value using colorama styles.

        Args:
            status (str): The status of the snapshot. Expected values are 'pending', 'complete', or 'deleted'.

        Returns:
            str: The status string wrapped in the appropriate colorama color code if the status is recognized,
                 otherwise returns the status string unchanged.

        Notes:
            - 'pending' is colored yellow.
            - 'complete' is colored green.
            - 'deleted' is colored red.
            - Any other status is returned without coloring.
        """
        match status:
            case 'pending':
                return yellow_text(status)
            case 'complete':
                return green_text(status)
            case 'deleted':
                return red_text(status)
            case _:
                return status
