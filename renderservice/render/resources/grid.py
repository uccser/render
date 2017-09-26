"""Module for generating Grid resource."""

from PIL import Image, ImageDraw


def resource(task, resource_manager):
    """Create a image for Grid resource.

    Args:
        task: Dicitionary of requested document options. (dict)
        resource_manager: File loader for external resources. (FileManager)

    Returns:
        A dictionary or list of dictionaries for each resource page.
    """
    GRID_COLUMNS = 8
    GRID_ROWS = 8
    BOX_SIZE = 500
    IMAGE_SIZE_X = BOX_SIZE * GRID_COLUMNS
    IMAGE_SIZE_Y = BOX_SIZE * GRID_ROWS
    LINE_COLOUR = "#000000"
    LINE_WIDTH = 3

    page = Image.new("RGB", (IMAGE_SIZE_X, IMAGE_SIZE_Y), "#fff")
    draw = ImageDraw.Draw(page)
    for x_coord in range(0, IMAGE_SIZE_X, BOX_SIZE):
        draw.line([(x_coord, 0), (x_coord, IMAGE_SIZE_Y)], fill=LINE_COLOUR, width=LINE_WIDTH)
    draw.line([(IMAGE_SIZE_X - 1, 0), (IMAGE_SIZE_X - 1, IMAGE_SIZE_Y)], fill=LINE_COLOUR, width=LINE_WIDTH)
    for y_coord in range(0, IMAGE_SIZE_Y, BOX_SIZE):
        draw.line([(0, y_coord), (IMAGE_SIZE_X, y_coord)], fill=LINE_COLOUR, width=LINE_WIDTH)
    draw.line([(0, IMAGE_SIZE_Y - 1), (IMAGE_SIZE_X, IMAGE_SIZE_Y - 1)], fill=LINE_COLOUR, width=LINE_WIDTH)

    return {"type": "image", "data": page}


def subtitle(task):
    """Return the subtitle string of the resource.

    Used after the resource name in the filename, and
    also on the resource image.

    Args:
        task: Dicitionary of requested document. (dict)

    Returns:
        text for subtitle. (str)
    """
    return task["paper_size"]


def valid_options():
    """Provide dictionary of all valid parameters.

    This excludes the header text parameter.

    Returns:
        All valid options. (dict)
    """
    return {
        "paper_size": ["a4", "letter"],
    }
