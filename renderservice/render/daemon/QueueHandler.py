"""Handles transactions with the taskqueue api."""
import json
import logging
from apiclient.discovery import build, HttpError
from base64 import b64encode, b64decode

logger = logging.getLogger(__name__)


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

    def __init__(self, project_id, location_id, taskqueue_id, discovery_url=None, credentials=None):
        """Create a new QueueHandler.

        Args:
            project_id: The project the taskqueue belongs to. (str)
            location_id: The location of the taskqueue. (str)
            taskqueue_id: The name of the taskqueue. (str)
        """
        self.project_id = project_id
        self.location_id = location_id
        self.taskqueue_id = taskqueue_id
        self.parent = "projects/{PROJECT_ID}/locations/{LOCATION_ID}/queues/{QUEUE_ID}".format(PROJECT_ID=project_id, LOCATION_ID=location_id, QUEUE_ID=taskqueue_id)

        if discovery_url is not None:
            self.client = build("cloudtasks", "v2beta2", discoveryServiceUrl=discovery_url, credentials=credentials)
        else:
            self.client = build("cloudtasks", "v2beta2", credentials=credentials)

    def __len__(self):
        """Count the number of tasks within the queue."""
        try:
            count = 0
            request = request_address(self.client).list(parent=self.parent)
            result = request.execute()
            if "tasks" in result.keys():
                count += len(result["tasks"])

            while "nextPageToken" in result.keys():
                request = request_address(client).list(parent=self.parent, pageToken=result["nextPageToken"])
                result = request.execute()
                if "tasks" in result.keys():
                    count += len(result["tasks"])

            return count
        except HttpError as http_error:
            logger.error("Error during get request: {}".format(http_error))
            return 0

    def get_task_payload(self, client, name):
        """Get the payload of a given task.

        Returns:
            A dictionary of the decoded task payload. (dict)
        """
        request_address = lambda client: client.projects().locations().queues().tasks()
        get_request = request_address(self.client).get(name=name, responseView="FULL")
        task_result = get_request.execute()
        return decode_dictionary(task_result["pullMessage"]["payload"])

    def tasks(self):
        """Get tasks within the taskqueue.

        Returns:
            A generator of Google Tasks as with the user defined
            task (dictionary) under that 'payload' key. (list of dicts)
        """
        request_address = lambda client: client.projects().locations().queues().tasks()
        try:
            request = request_address(self.client).list(parent=self.parent)
            result = request.execute()
            if "tasks" in result.keys():
                for task in result["tasks"]:
                    payload = self.get_task_payload(self.client, task["name"])
                    task["payload"] = payload
                    yield task

            while "nextPageToken" in result.keys():
                request = request_address(self.client).list(parent=self.parent, pageToken=result["nextPageToken"])
                result = request.execute()
                if "tasks" in result.keys():
                    for task in result["tasks"]:
                        payload = self.get_task_payload(self.client, task["name"])
                        task["payload"] = payload
                        yield task

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
        request_address = lambda client: client.projects().locations().queues().tasks()
        try:
            task = {
                "task": {
                    "pullMessage": {
                        "payload": encode_dictionary(task_payload)
                    }
                }
            }
            if tag is not None:
                task["task"]["pullMessage"]["tag"] = b64encode(tag.encode("ascii")).decode()

            request = request_address(self.client).create(parent=self.parent, body=task)
            result = request.execute()
            return result["name"]
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
            A generator of Google Tasks as with the user defined
            task (dictionary) under that 'payload' key. (list of dicts)
        """
        request_address = lambda client: client.projects().locations().queues().tasks()
        try:
            if tag is None:
                tag = "oldest_tag()"
            # else:
            #    tag = tag.replace("\\", "\\\\").replace("\"", "\\\"")

            body = {
                "maxTasks": tasks_to_fetch,
                "leaseDuration": "{}s".format(lease_secs),
                "responseView": "BASIC",
                "filter": "tag={}".format(tag),
            }
            request = request_address(self.client).pull(name=self.parent, body=body)
            result = request.execute()

            if "tasks" in result.keys():
                for task in result["tasks"]:
                    payload = self.get_task_payload(self.client, task["name"])
                    task["payload"] = payload
                    yield task

            while "nextPageToken" in result.keys():
                request = request_address(self.client).pull(parent=self.parent, pageToken=result["nextPageToken"])
                result = request.execute()
                if "tasks" in result.keys():
                    for task in result["tasks"]:
                        payload = self.get_task_payload(self.client, task["name"])
                        task["payload"] = payload
                        yield task

        except HttpError as http_error:
            logger.error("Error during lease request: {}".format(http_error))
            return []

    def renew_lease(self, task_id, scedule_time, new_lease_secs):
        """Update a task lease from the taskqueue.

        Args:
            task_id: A string of the task_id. (str)
            scedule_time: The task's current schedule time, available in
                the task["schedule_time"]. This restriction is to check
                that the caller is renewing the correct task.
            new_lease_secs: The number of seconds to update the lease
                by. (int)
        Returns:
            The updated Google Task as a dictionary, the payload is
            untouched. If there is an error None is returned. (dict)
        """
        request_address = lambda client: client.projects().locations().queues().tasks()
        try:
            body = {
                "scheduleTime": scedule_time,
                "newLeaseDuration": "{}s".format(new_lease_secs),
                "responseView": "BASIC"
            }
            request = request_address(self.client).renewLease(name=task_id, body=body)
            result = request.execute()
            return result
        except HttpError as http_error:
            logger.error("Error during lease request: {}".format(http_error))
            return None

    def acknowledge_task(self, task_id):
        """Acknowledge a task is completed.

        Args:
            task_id: A string of the task_id. (str)
        Returns:
            True if the acknowledge was successful, False otherwise. (bool)
        """
        request_address = lambda client: client.projects().locations().queues().tasks()
        try:
            request = request_address(self.client).acknowledge(name=task_id)
            result = request.execute()
            return not bool(result)  # Empty dictionarys evaluate to False
        except HttpError as http_error:
            logger.error("Error during delete request: {}".format(http_error))
        return False

    def delete_task(self, task_id):
        """Delete a task from the taskqueue.

        Args:
            task_id: A string of the task_id. (str)
        Returns:
            True if the delete was successful, False otherwise. (bool)
        """
        request_address = lambda client: client.projects().locations().queues().tasks()
        try:
            request = request_address(self.client).delete(name=task_id)
            result = request.execute()
            return not bool(result)  # Empty dictionarys evaluate to False
        except HttpError as http_error:
            logger.error("Error during delete request: {}".format(http_error))
        return False
