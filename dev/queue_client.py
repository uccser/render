"""Allows access to queue in order to create tasks and get results.

You will need to install from the renderservice
  pip install -r requirements.txt
"""

import base64
import importlib.machinery
import sys
import optparse
import os


# Local Queue Code
def get_queue_host():
    """Get the IP Address of the queue host.

    Using the command:
        docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' render_queue_1

    Returns:
        A string of the IP address
    """
    import subprocess
    command = [
        'docker',
        'inspect',
        '-f',
        '\'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}\'',
        'render_queue_1'
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    return result.stdout.decode().strip('\n\'')


PROJECT_NAME = "cs-unplugged-develop"
QUEUE_NAME = "render-queue"

QUEUE_HOST = get_queue_host()
DISCOVERY_URL = "http://{}:5052/api/{{api}}/{{apiVersion}}".format(QUEUE_HOST)
CREDENTIALS = None


# Online Queue Code
def get_credentials():
    """Get credentials to log into online taskqueue."""
    from oauth2client.service_account import ServiceAccountCredentials
    client_secret_file = 'client.json'
    scopes = ['https://www.googleapis.com/auth/cloud-platform']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(client_secret_file, scopes)
    return credentials


PROJECT_NAME = "render-181102"
LOCATION = "us-central1"
QUEUE_NAME = "render"
DISCOVERY_URL = "https://cloudtasks.googleapis.com/$discovery/rest?version=v2beta2"
CREDENTIALS = get_credentials()


def parse_args():
    """Command-line option parser for program control."""
    opts = optparse.OptionParser(
        usage="{0} [options] [command]".format(sys.argv[0]),
        description="Access and manipulate queue, where the"
        "commands can be add, list, lease, document, flush.")
    # Configure options
    # opts.add_option("--key-file", "-k", action="store",
    #     type="string", help="Location of the credentials file.",
    #     default=None)
    options, arguments = opts.parse_args()
    # Extra option parsing

    # Return options
    return options, arguments


def action_add(queue):
    """Add a render task to the given queue.

    Please modify this as needed.

    Args:
        queue: QueueHandler to interact with.
    """
    queue.create_task({
        "kind": "task#render",
        "resource_slug": "binary-cards",
        "resource_name": "Binary Cards",
        "resource_view": "binary_cards",
        "url": "resources/binary-cards.html",
        "display_numbers": False,
        "black_back": True,
        "paper_size": "a4",
        "header_text": "",
        "copies": 1,
    }, tag="task")


def action_list(queue):
    """List up to 100 tasks in the queue.

    Args:
        queue: QueueHandler to interact with.
    """
    tasks = list(queue.tasks())
    print("Number of tasks: {}".format(len(tasks)))
    for task in tasks:
        print(task)


def action_lease(queue):
    """Lease tasks tagged with task from the queue for 30 seconds.

    Args:
        queue: QueueHandler to interact with.
    """
    tasks = list(queue.lease_tasks(tasks_to_fetch=100, lease_secs=30, tag="task"))
    print("Number of tasks: {}".format(len(tasks)))
    for task in tasks:
        print(task)


def action_document(queue):
    """Save out document results from the queue.

    Args:
        queue: QueueHandler to interact with.
    """
    tasks = queue.list_tasks()
    for task in tasks:
        if task["payload"]["kind"] == "result#document":
            data = task["payload"]["document"].encode("ascii")
            document = base64.b64decode(data)
            filename = task["payload"]["filename"]
            with open(filename, "wb") as f:
                f.write(document)


def action_flush(queue):
    """Attempt to delete all tasks from the queue.

    Args:
        queue: QueueHandler to interact with.
    """
    tasks = queue.tasks()
    for task in tasks:
        queue.delete_task(task["name"])


if __name__ == "__main__":
    options, arguments = parse_args()

    directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'renderservice/render/daemon/QueueHandler.py'))
    loader = importlib.machinery.SourceFileLoader('render.daemon', directory)
    handle = loader.load_module('render.daemon')

    queue = handle.QueueHandler(project_id=PROJECT_NAME, location_id=LOCATION,
                                taskqueue_id=QUEUE_NAME, discovery_url=DISCOVERY_URL,
                                credentials=CREDENTIALS)

    action = arguments[0]
    if action == "add":
        action_add(queue)
    elif action == "list":
        action_list(queue)
    elif action == "lease":
        action_lease(queue)
    elif action == "document":
        action_document(queue)
    elif action == "flush":
        action_flush(queue)
