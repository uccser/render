"""Module for generating Barcode Checksum Poster resource."""

from PIL import Image


def resource(task, resource_manager):
    """Create a image for Barcode Checksum Poster resource.

    Args:
        task: Dicitionary of requested document options.
        resource_manager: File loader for external resources.

    Returns:
        A dictionary or list of dictionaries for each resource page.
    """
    # Retrieve parameters
    parameter_options = valid_options()
    barcode_length = task["barcode_length"]

    image_path = "img/resources/barcode-checksum-poster/{}-digits.png"
    data = resource_manager.load(image_path.format(barcode_length))
    image = Image.open(data)
    return {"type": "image", "data": image}


def subtitle(task):
    """Return the subtitle string of the resource.

    Used after the resource name in the filename, and
    also on the resource image.

    Args:
        task: Dicitionary of requested document.

    Returns:
        text for subtitle (str).
    """
    barcode_length = task["barcode_length"]
    paper_size = task["paper_size"]
    return "{} digits - {}".format(barcode_length, paper_size)


def valid_options():
    """Provide dictionary of all valid parameters.

    This excludes the header text parameter.

    Returns:
        All valid options (dict).
    """
    return {
        "barcode_length": ["12", "13"],
        "paper_size": ["a4", "letter"],
    }
