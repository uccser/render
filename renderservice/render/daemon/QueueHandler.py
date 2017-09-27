"""Handles transactions with the taskqueue api."""
import json
import logging
import httplib2shim
from apiclient.discovery import build, HttpError
from base64 import b64encode, b64decode

logger = logging.getLogger(__name__)


def authorize_session():
    """Authorize for taskqueue transactions.

    Returns:
        Something in future!
    """
    pass  # TODO
    # Should probably just use https://developers.google.com/identity/protocols/application-default-credentials
    from oauth2client.client import GoogleCredentials
    credentials = GoogleCredentials.get_application_default()
    return credentials


def encode_dictionary(dictionary):
    """Encode a dictionary into a base64 string.

    Args:
        dictionary: A python dictionary to convert. (dict)
    Returns:
        The encoded string. (base64 string)
    """
    string = json.dumps(dictionary)
    encoded_string = b64encode(string.encode("ascii")).decode()
    return encoded_string


def decode_dictionary(encoded_string):
    """Decode a base64 string into a dictionary.

    Args:
        encoded_string: A base64 string to decode. (base64 string)
    Returns:
        A python dictionary deserialized from the string. (dict)
    """
    string = b64decode(encoded_string).decode()
    dictionary = json.loads(string)
    return dictionary


class QueueHandler(object):
    """Handles transactions with the taskqueue api."""

    def __init__(self, project_name, taskqueue_name, discovery_url=None):
        """Create a new QueueHandler.

        Args:
            project_name: The project the taskqueue belongs to. (str)
            taskqueue_name: The name of the taskqueue. (str)
        """
        self.project_name = project_name
        self.taskqueue_name = taskqueue_name

        http = httplib2shim.Http()
        if discovery_url is not None:
            self.task_api = build("taskqueue", "v1beta2", http=http, discoveryServiceUrl=discovery_url)
        else:
            self.task_api = build("taskqueue", "v1beta2", http=http)

    def __len__(self):
        """Count the number of tasks within the queue."""
        try:
            get_request = self.task_api.taskqueues().get(
                project=self._get_project_name(False),
                taskqueue=self.taskqueue_name,
                getStats=True
            )
            result = get_request.execute()
            return result["stats"]["totalTasks"]
        except HttpError as http_error:
            logger.error("Error during get request: {}".format(http_error))
            return 0

    def _get_project_name(self, is_write):
        """Get the project name based for write command.

        Args:
            is_write: A boolean determining if the name will be used
                for a write operation. (bool)
        Returns:
            A string of the project name required for a task_api call. (str)
        """
        if is_write:
            return "b~" + self.project_name
        return self.project_name

    def list_tasks(self):
        """List some tasks within the taskqueue.

        Returns:
            A list of Google Tasks as with the user defined
            task (dictionary) under that 'payload' key. (list of dicts)
        """
        try:
            tasks = []
            list_request = self.task_api.tasks().list(
                project=self._get_project_name(False),
                taskqueue=self.taskqueue_name
            )
            result = list_request.execute()
            if result["kind"] == "taskqueue#tasks":
                for task in result["items"]:
                    task["payload"] = decode_dictionary(task["payloadBase64"])
                    tasks.append(task)
            elif result["kind"] == "taskqueues#task":
                task["payload"] = decode_dictionary(result["payloadBase64"])
                tasks.append(task)
            return tasks
        except HttpError as http_error:
            logger.error("Error during lease request: {}".format(http_error))
            return []

    def create_task(self, task_payload, tag=None):
        """Create a new task and places it on the taskqueue.

        Args:
            task_payload: A dictionary describing the task. (dict)
            tag: A tag attached to the task. (str)
        Returns:
            The task id of the created task, otherwise None if error. (str)
        """
        try:
            task = {
                "kind": "taskqueues#task",
                "queueName": self.taskqueue_name,
                "payloadBase64": encode_dictionary(task_payload)
            }
            if tag is not None:
                task["tag"] = tag

            insert_request = self.task_api.tasks().insert(
                project=self._get_project_name(True),
                taskqueue=self.taskqueue_name,
                body=task
            )
            result = insert_request.execute()
            return result["id"]
        except HttpError as http_error:
            logger.error("Error during insert request: {}".format(http_error))
            return None

    def lease_tasks(self, tasks_to_fetch, lease_secs, tag=None):
        """Lease tasks from the taskqueue.

        Args:
            tasks_to_fetch: The number of tasks to fetch. (int)
            lease_secs: The number of seconds to lease for. (int)
            tag: the tag to restrict leasing too. (str)
        Returns:
            A list of Google Tasks as with the user defined
            task (dictionary) under that 'payload' key. (list of dicts)
        """
        try:
            tasks = []
            lease_request = self.task_api.tasks().lease(
                project=self._get_project_name(True),
                taskqueue=self.taskqueue_name,
                leaseSecs=lease_secs,
                numTasks=tasks_to_fetch,
                groupByTag=tag is not None,
                tag=tag
            )
            result = lease_request.execute()
            if result["kind"] == "taskqueue#tasks":
                for task in result["items"]:
                    task["payload"] = decode_dictionary(task["payloadBase64"])
                    tasks.append(task)
            elif result["kind"] == "taskqueues#task":
                task["payload"] = decode_dictionary(result["payloadBase64"])
                tasks.append(task)
            return tasks
        except HttpError as http_error:
            logger.error("Error during lease request: {}".format(http_error))
            return []

    def update_task(self, task_id, new_lease_secs):
        """Update a task lease from the taskqueue.

        Args:
            task_id: A string of the task_id. (str)
            new_lease_secs: The number of seconds to update the lease
                by. (int)
        Returns:
            The updated Google Task as a dictionary, the payload is
            untouched. If there is an error None is returned. (dict)
        """
        try:
            task = {
                "queueName": self.taskqueue_name
            }
            patch_request = self.task_api.tasks().patch(
                project=self._get_project_name(True),
                taskqueue=self.taskqueue_name,
                newLeaseSeconds=new_lease_secs,
                task=task_id,
                body=task
            )
            result = patch_request.execute()
            return result
        except HttpError as http_error:
            logger.error("Error during lease request: {}".format(http_error))
            return None

    def delete_task(self, task_id):
        """Delete a task from the taskqueue.

        Args:
            task_id: A string of the task_id. (str)
        Returns:
            True if the delete was successful, False otherwise. (bool)
        """
        try:
            delete_request = self.task_api.tasks().delete(
                project=self._get_project_name(True),
                taskqueue=self.taskqueue_name,
                task=task_id
            )
            delete_request.execute()
            return True
        except HttpError as http_error:
            logger.error("Error during delete request: {}".format(http_error))
        return False
