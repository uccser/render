"""Module for generating Treasure Hunt resource."""

from PIL import Image, ImageDraw, ImageFont
from random import sample


def resource(task, resource_manager):
    """Create a image for Treasure Hunt resource.

    Args:
        task: Dicitionary of requested document options. (dict)
        resource_manager: File loader for external resources. (FileManager)

    Returns:
        A dictionary or list of dictionaries for each resource page.
    """
    pages = []
    IMAGE_PATH = "img/resources/treasure-hunt/{}.png"
    FONT_PATH = "fonts/PatrickHand-Regular.ttf"
    local_font_path = resource_manager.get_path(FONT_PATH)

    # Add numbers to image if required
    prefilled_values = task["prefilled_values"]
    number_order = task["number_order"]
    instructions = task["instructions"]
    art_style = task["art"]

    if instructions:
        data = resource_manager.load(IMAGE_PATH.format("instructions"))
        image = Image.open(data)
        ImageDraw.Draw(image)
        pages.append({"type": "image", "data": image})

    data = resource_manager.load(IMAGE_PATH.format(art_style))
    image = Image.open(data)
    draw = ImageDraw.Draw(image)

    # Add numbers to image if required
    if prefilled_values != "blank":
        (range_min, range_max, font_size) = number_range(task)
        font = ImageFont.truetype(local_font_path, font_size)

        total_numbers = 26
        numbers = sample(range(range_min, range_max), total_numbers)
        if number_order == "sorted":
            numbers.sort()

        base_coord_y = 506
        coord_y_increment = 199
        base_coords_x = [390, 700]
        for i in range(0, total_numbers):
            text = str(numbers[i])
            text_width, text_height = draw.textsize(text, font=font)

            coord_x = base_coords_x[i % 2] - (text_width / 2)
            coord_y = base_coord_y - (text_height / 2)
            if i % 2 == 1:
                coord_y -= 10
                base_coord_y += coord_y_increment
            draw.text(
                (coord_x, coord_y),
                text,
                font=font,
                fill="#000"
            )

        text = "{} - {} to {}".format(number_order.title(), range_min, range_max - 1)
        font = ImageFont.truetype(local_font_path, 75)
        text_width, text_height = draw.textsize(text, font=font)
        coord_x = 1220 - (text_width / 2)
        coord_y = 520 - (text_height / 2)
        draw.text(
            (coord_x, coord_y),
            text,
            font=font,
            fill="#000",
        )
    pages.append({"type": "image", "data": image})

    return pages


def subtitle(task):
    """Return the subtitle string of the resource.

    Used after the resource name in the filename, and
    also on the resource image.

    Args:
        task: Dicitionary of requested document. (dict)

    Returns:
        text for subtitle. (str)
    """
    prefilled_values = task["prefilled_values"]
    art_style = task["art"]
    instructions = task["instructions"]
    paper_size = task["paper_size"]

    if prefilled_values == "blank":
        range_text = "blank"
    else:
        SUBTITLE_TEMPLATE = "{} - {} to {}"
        number_order_text = task["number_order"].title()
        range_min, range_max, font_size = number_range(task)
        range_text = SUBTITLE_TEMPLATE.format(number_order_text, range_min, range_max - 1)

    if art_style == "colour":
        art_style_text = "full colour"
    else:
        art_style_text = "black and white"

    if instructions:
        instructions_text = "with instructions"
    else:
        instructions_text = "without instructions"

    return "{} - {} - {} - {}".format(range_text, art_style_text, instructions_text, paper_size)


def number_range(task):
    """Return number range tuple for resource.

    Args:
        task: Dicitionary of requested document. (dict)

    Returns:
        Tuple of range_min, range_max, font_size. (tuple)
    """
    prefilled_values = task["prefilled_values"]
    range_min = 0
    if prefilled_values == "easy":
        range_max = 100
        font_size = 55
    elif prefilled_values == "medium":
        range_max = 1000
        font_size = 50
    elif prefilled_values == "hard":
        range_max = 10000
        font_size = 45
    return (range_min, range_max, font_size)


def valid_options():
    """Provide dictionary of all valid parameters.

    This excludes the header text parameter.

    Returns:
        All valid options. (dict)
    """
    return {
        "prefilled_values": ["blank", "easy", "medium", "hard"],
        "number_order": ["sorted", "unsorted"],
        "instructions": [True, False],
        "art": ["colour", "bw"],
        "paper_size": ["a4", "letter"],
    }
