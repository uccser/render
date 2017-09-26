Developer Documentation
##############################################################################

The following pages are for those wanting to develop the render service.

.. toctree::
    :maxdepth: 1
    :caption: Contents

    render
    queue
    resource


Overview
=============================================================================

Both the CS Unplugged and CS Field Guide projects include resources which need to be generated on the fly.
These range from converting a page into a printer-friendly state, to generating unique classroom worksheets using a base template.
To avoid putting uneccessary load on the client, we do this using our "Render Service".

This system is split into two parts; the ``queueservice`` and the ``renderservice`` itself.

The `queueservice` is essentially a temporary hack while we wait for the Google Task Queue v2 to be released, assuming it is suitable to run it localy.
It is responsible for recieving tasks from the ***SOMETHING*** and sending them to the ``renderservice`` while developing locally.

The ``renderservice`` is the component that is actually responsible for generating resources based on tasks it recieves from the task queue.
The ``renderserice`` also contains the resources used in the CS Unplugged project.


Glossary
=============================================================================

Before reading these docs, these are the terms you'll want to familiarise yourself with:

  - Task (our task and google task)
    There are two kind of tasks, a task from Google and a task from us. The simplist way to differ between the two is our task is the payload of a Google task.
  - Resource
