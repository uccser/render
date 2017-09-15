# You will need to install from the renderservice
#   pip install -r requirements.txt
#   pip install -e render

import importlib.machinery
import sys
import os

PROJECT_NAME = "cs-unplugged"
QUEUE_NAME = "render-queue"
DISCOVERY_URL = "http://localhost:5052/api/{api}/{apiVersion}"

def action_add(queue):
    queue.create_task({
        "kind": "task#render",
        "resource_slug": "treasure-hunt",
        "resource_name": "Treasure Hunt",
        "resource_view": "treasure_hunt",
        "url": "resources/treasure-hunt.html",
        "prefilled_values": "blank",
        "number_order": "sorted",
        "paper_size": "a4",
        "header_text": "",
        "copies": 1,
    })

def action_list(queue):
    tasks = queue.list_tasks()
    print("Number of tasks: {}".format(len(tasks)))
    for task in tasks:
        print(task["payload"])

def action_document(queue):
    pass

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
    elif action == "document":
        action_document(queue)
