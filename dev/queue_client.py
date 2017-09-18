# You will need to install from the renderservice
#   pip install -r requirements.txt

import base64
import importlib.machinery
import sys
import os


PROJECT_NAME = "cs-unplugged-develop"
QUEUE_NAME = "render-queue"
DISCOVERY_URL = "http://localhost:5052/api/{api}/{apiVersion}"


def action_add(queue):
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
    tasks = queue.list_tasks()
    print("Number of tasks: {}".format(len(tasks)))
    for task in tasks:
        print(task)


def action_lease(queue):
    tasks = queue.lease_tasks(tasks_to_fetch=100, lease_secs=60, tag="task")
    print("Number of tasks: {}".format(len(tasks)))
    for task in tasks:
        print(task)


def action_document(queue):
    tasks = queue.list_tasks()
    for task in tasks:
        if task["payload"]["kind"] == "result#document":
            data = task["payload"]["document"].encode("ascii")
            document = base64.b64decode(data)
            filename = task["payload"]["filename"]
            with open(filename, "wb") as f:
                f.write(document)


def action_flush(queue):
    tasks = queue.list_tasks()
    while len(tasks) > 0:
        for task in tasks:
            queue.delete_task(task["id"])

        tasks = queue.list_tasks()


if __name__ == "__main__":
    directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'renderservice/render/daemon/QueueHandler.py'))
    loader = importlib.machinery.SourceFileLoader('render.daemon', directory)
    handle = loader.load_module('render.daemon')

    queue = handle.QueueHandler(project_name=PROJECT_NAME, taskqueue_name=QUEUE_NAME, discovery_url=DISCOVERY_URL)
    action = sys.argv[1]

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
