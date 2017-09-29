Render Service
##############################################################################

The render service pipline flows as follows; It accesses an external queue to get a task, consumes the task creating a resource, saves the resource and then repeats this process. Input tasks that are consumed are tagged with :code:`task` and output is handled by tasks with the :code:`result` tag.

Task Definitions
==============================================================================

Tasks retrieved from the render queue must be a json dictionary. That is, using the json library python must be able to load the payload as a dictionary. This dictionary must also contain a :code:`kind` mapping which specifies what can be done with the message.

General Tasks
------------------------------------------------------------------------------

These tasks must be tagged with the :code:`task` string when added to the queue. The render service only consumes tasks that are tagged with :code:`task`.

To render a resource you must use the :code:`render` task as defined below.

.. code-block:: none

  {
    kind: "task#render"
    resource_slug: string,
    resource_name: string,
    resource_view: string,
    url: string
    header_text: string,
    copies: 1
  }

Where all of the above are required for every task, and for each resource additional values may be required based on their :code:`valid_options` function.

The :code:`resource_view` determines the resource module to generate from, the :code:`resource_slug` and :code:`resource_name` are arbitary strings, the :code:`url` is preferably the url where the resource was generated from (including query), the :code:`header_text` is a string either an empty string or arbitary, and finally the :code:`copies` determines how many to generate.

Result Tasks
------------------------------------------------------------------------------
These tasks must be tagged with the :code:`result` string when added to the queue. The render service produces these tasks when a generate task has been completed to instruct other services where to find the output file.

For documents that are small enough to be placed within the queue, the following task will be defined:

.. code-block:: none

  {
    kind: "result#document"
    success: boolean
    filename: string
    document: base64 string
  }

Where :code:`success` is a boolean determining if the associated task was completed correctly, :code:`filename` is the filename of document, :code:`document` is a base64 encoded string of the document bytes.

Another possible result is the is a document that is saved externally and a url can be used to access it, these tasks are defined as follows:

.. code-block:: none

  {
    kind: "result#link"
    success: boolean
    url: string
  }

Where :code:`success` is a boolean determining if the associated task was completed correctly, and :code:`url` is the address to access the document.

Infrastructure
==============================================================================

The render service consists of multiple processes on a single unit, this includes multiple daemons that consume tasks from an external queue and produce files, and a webserver performs health checks that monitor and restart the render daemons.

Important files:

.. code-block:: none

  renderservice/
  ├── render/
  |   ├── daemon/
  |   ├── resources/
  |   ├── tests/
  |   ├── webserver/
  |   └── __init__.py
  ├── scripts/
  |   ├── docker-entrypoint.sh
  |   ├── mount-bucket.sh
  |   ├── pip-install.sh
  |   └── shutdown-script.sh
  ├── static/
  ├── templates/
  ├── Dockerfile
  ├── Dockerfile-local
  ├── requirements.txt


- ``render/``: The python render service package.

  + ``daemon/``: Contains python classes pertaining to the daemon for consuming tasks and producing files.
  + ``resources/``: Contains source files with custom logic for generating resources (pdf files).
  + ``tests/``: Tests covering all the logic in the python render service package.
  + ``webserver/``: Contains the webserver logic, including logic for health checks and daemon recovery.
  + ``__init__.py``: Contains the version of the render service.

- ``scripts/``: Bash shell scripts used in the creation of the render service.

  + ``docker-entrypoint.sh``: The entrypoint for the render service, creates multiple daemons and starts up the webservice.
  + ``mount-bucket.sh``: Mounts the Google Cloud bucket using `gcsfuse <https://cloud.google.com/storage/docs/gcs-fuse>`_.
  + ``pip-install.sh``: Installs a pip requirements file in a specific order.
  + ``shutdown-script.sh``: TODO: This is still to be used. A script which is run when the machine is pre-empted.

- ``static/``: Locally stored static files, either kept locally for speed or licence reasons (such as do not distribute).
- ``templates/``: Jinja templates for webpages and render service.
- ``Dockerfile``: Dockerfile for building the service.
- ``Dockerfile-local``: Dockerfile for building the service for local development.
- ``requirements.txt``: Specifies required python modules needed to run the webservice.

Some important things to note when working with the render service:

- When in local development the render service does not have a live volume of the renderservice directory, that mean any changes require a rebuild of the service to see the changes.

- The render service has multiple directories for static files, a local copy and a mounted external copy. The static folder in the root directory of the repository is mounted as the external copy when run locally.
