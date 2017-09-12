Render Service
##############################################################################

The render service pipline flows as follows; It accesses an external queue to get a task, consumes the task creating a resource, saves the resource and then repeats this process.

Infrastructure
==============================================================================

The render service consists of multiple processes on a single unit, this includes multiple daemons that consume tasks from an external queue and produce files, and a webserver that allows from health checks that monitor and restart the render daemons.

Important files:

.. code-block:: none

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
  ├── .coveragerc
  ├── Dockerfile
  ├── Dockerfile-local
  ├── requirements.txt
  └── setup.cfg


- ``render/``: The python render service package.

  + ``daemon/``: Contains python classes pertaining to the daemon for consuming tasks and producing files.
  + ``resources/``: Contains source files with custom logic for generating resources (pdf files).
  + ``tests/``: Tests covering all the logic in the python render service package.
  + ``webserver/``: Contains the webserver logic, including logic for health checks and daemon recovery.
  + ``__init__.py``: Contains the version of the render service.

- ``scripts/``: Bash shell scripts used in the creation of the render service.

  + ``docker-entrypoint.sh``: The entrypoint for the render service, creates multiple daemons and starts up the webservice.
  + ``mount-bucket.sh``: Mounts the Google Cloud bucket using gfuze.
  + ``pip-install.sh``: Installs a pip requirements file in a specific order.
  + ``shutdown-script.sh``: TODO: This is still to be used. A script which is run when the machine is pre-empted.

- ``static/``: Locally stored static files, either kepted locally for speed or licence reasons (such as do not distribute).
- ``templates/``: Jinja templates for webpages and render service.
- ``.coveragerc``: Configuration for coverage reporting.
- ``Dockerfile``: Dockerfile for building the service.
- ``Dockerfile-local``: Dockerfile for building the service for local development.
- ``requirements.txt``: Specifies required python modules needed to run the webservice.
- ``setup.cfg``: Configuration file for style services such as flake8 and pydocstyle.

Some important things to note when working with the render service:

- When in local development the render service does not have a live volume of the renderservice directory, that mean any changes require a rebuild of the service to see the changes.

- The render service has multiple directories for static files, a local copy and a mounted external copy. The static folder in the root directory of the repository is mounted as the external copy when run locally. 
