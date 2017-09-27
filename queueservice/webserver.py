"""Webserver for the queue service."""
import os
import logging
import json
from flask import Flask
from api_data.taskqueue_v1beta2 import taskqueue_v1beta2_api


# FLASK SETUP

HOST = os.getenv("NETWORK_IPADDRESS", "localhost")
PORT = int(os.getenv("PORT", 5052))
application = Flask(__name__)
application.register_blueprint(taskqueue_v1beta2_api, url_prefix="/taskqueue/v1beta2/projects")


@application.route("/")
def index():
    """Give index page describing the service."""
    return "CS-Unplugged - Fake Google TaskQueue"


@application.route("/api/<api>/<version>")
def api(api=None, version=None):
    """Get an API description that is stored in data.

    The API will be a modified copy (usually to remove authorization
    requirements) of the original from the mimicked source.

    Args:
        api: The string of the api to load. (str)
        version: The string of the version of the api to load. (str)
    Returns:
        A JSON object describing the API.
    """
    content = None
    filepath = os.path.join("api_data", "{0}_{1}.api".format(api, version))
    if not os.path.exists(filepath):
        message = "API does not exist for {} version {}.".format(api, version)
        logging.exception(message)
        return message, 404
    elif not os.path.isfile(filepath):
        message = "Server Error: API path exists for {} (version {}) but is not a file.".format(api, version)
        logging.exception(message)
        return message, 500
    with open(filepath, "r") as f:
        api_json = json.loads(f.read())
        api_json["baseUrl"] = "http://{}:{}/{}/{}/projects/".format(HOST, PORT, api, version)
        api_json["basePath"] = "/{}/{}/projects/".format(api, version)
        api_json["rootUrl"] = "http://{}:{}/".format(HOST, PORT)
        api_json["servicePath"] = "{}/{}/projects/".format(api, version)
        content = json.dumps(api_json)
    return content


@application.errorhandler(500)
def server_error(e):
    """Log and reports back information about internal errors.

    Args:
        e: The exception which was raised. (Exception)
    Returns:
        A string which describes the exception and the internal server
        error status code.
    """
    logging.exception("An error occurred during a request.")
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0", port=PORT)
