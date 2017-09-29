"""Module for generating Sorting Network Cards resource."""

import os
from random import sample
from PIL import Image, ImageDraw, ImageFont


def resource(task, resource_manager):
    """Create a image for Sorting Network Cards resource.

    Args:
        task: Dicitionary of requested document options. (dict)
        resource_manager: File loader for external resources. (FileManager)

    Returns:
        A dictionary or list of dictionaries for each resource page.
    """
    IMAGE_SIZE_X = 2000
    IMAGE_SIZE_Y = 3000
    LINE_COLOUR = "#000000"
    LINE_WIDTH = 3

    font_path = "fonts/PatrickHand-Regular.ttf"
    local_font_path = resource_manager.get_path(font_path)
    font_size = 300

    # Retrieve parameters
    card_type = task["type"]

    # Create card outlines
    card_outlines = Image.new("RGB", (IMAGE_SIZE_X, IMAGE_SIZE_Y), "#fff")
    draw = ImageDraw.Draw(card_outlines)
    for x_coord in range(0, IMAGE_SIZE_X, IMAGE_SIZE_X - LINE_WIDTH):
        draw.line([(x_coord, 0), (x_coord, IMAGE_SIZE_Y)], fill=LINE_COLOUR, width=LINE_WIDTH)
    for y_coord in range(0, IMAGE_SIZE_Y, int(IMAGE_SIZE_Y / 2 - LINE_WIDTH)):
        draw.line([(0, y_coord), (IMAGE_SIZE_X, y_coord)], fill=LINE_COLOUR, width=LINE_WIDTH)

    # Prepare text data
    card_data_type = "text"
    if card_type == "small_numbers":
        font_size = 800
        text = ["1", "2", "3", "4", "5", "6"]
    elif card_type == "large_numbers":
        font_size = 500
        text = []
        numbers = sample(range(1700000, 2100000), 6)
        for number in numbers:
            text.append("{:,}".format(number))
    elif card_type == "fractions":
        font_size = 900
        font_path = "fonts/NotoSans-Regular.ttf"
        local_font_path = resource_manager.get_path(font_path)
        text = [u"\u00bd", u"\u2153", u"\u2154", u"\u215c", u"\u00be", u"\u215d"]
    elif card_type == "maori_numbers":
        font_size = 300
        text = [
            "tahi", "rua", "toru", "whā", "rima", "ono", "whitu", "waru",
            "iwa", "tekau", "tekau mā tahi", "tekau mā waru", "tekau mā toru",
            "tekau mā whā", "rua tekau", "rua tekau mā ono"
        ]
    elif card_type == "words":
        font_size = 500
        text = ["crocodile", "crochet", "kiwi", "weka", "kiwi", "kiwano"]
    elif card_type == "letters":
        font_size = 800
        text = ["L", "O", "N", "K", "E", "D", "S", "P", "G", "B", "I", "Y"]
    elif card_type == "maori_colours":
        font_size = 500
        text = [
            "whero", "kākāriki", "kiwikiwi", "karaka",
            "kōwhai", "pango", "māwhero", "mā"
        ]
    elif card_type == "riding_hood":
        card_data_type = "image"
        images = [
            "little-red-riding-hood-1.png",
            "little-red-riding-hood-2.png",
            "little-red-riding-hood-3.png",
            "little-red-riding-hood-4.png",
            "little-red-riding-hood-5.png",
            "little-red-riding-hood-6.png",
        ]
    elif card_type == "butterfly":
        card_data_type = "image"
        images = [
            "butterfly-story-leaf.png",
            "butterfly-story-baby-caterpillar.png",
            "butterfly-story-caterpillar.png",
            "butterfly-story-young-pupa.png",
            "butterfly-story-mature-pupa.png",
            "butterfly-story-butterfly.png",
        ]

    card_centers = [
        (IMAGE_SIZE_X / 2, IMAGE_SIZE_Y / 4),
        (IMAGE_SIZE_X / 2, (IMAGE_SIZE_Y / 4) * 3),
    ]

    # Add text to cards
    pages = []
    if card_data_type == "image":
        IMAGE_PADDING = 20
        MAX_IMAGE_X = IMAGE_SIZE_X - IMAGE_PADDING * 2
        MAX_IMAGE_Y = IMAGE_SIZE_Y / 2 - IMAGE_PADDING * 2
        BASE_PATH = "img/resources/sorting-network-cards/"
        for (image_number, filename) in enumerate(images):
            data = resource_manager.load(os.path.join(BASE_PATH, filename))
            image = Image.open(data)
            (width, height) = image.size
            if height > MAX_IMAGE_Y or width > MAX_IMAGE_X:
                height_ratio = MAX_IMAGE_Y / height
                width_ratio = MAX_IMAGE_X / width
                ratio = min(height_ratio, width_ratio)
                width *= ratio
                height *= ratio
                image = image.resize((int(width), int(height)), Image.ANTIALIAS)
            if image_number % 2 == 0:
                page = card_outlines.copy()
                draw = ImageDraw.Draw(page)
                (x, y) = card_centers[0]
            else:
                (x, y) = card_centers[1]
            coords = (int(x - (width / 2)), int(y - (height / 2)))
            page.paste(image, box=coords, mask=image)
            # If image on second card but not last page
            if image_number % 2 == 1 and image_number != len(images) - 1:
                pages.append({"type": "image", "data": page})
    else:
        font = ImageFont.truetype(local_font_path, font_size)
        for (text_number, text_string) in enumerate(text):
            if text_number % 2 == 0:
                page = card_outlines.copy()
                draw = ImageDraw.Draw(page)
                (x, y) = card_centers[0]
            else:
                (x, y) = card_centers[1]

            text_width, text_height = draw.textsize(text_string, font=font)
            coord_x = x - (text_width / 2)
            coord_y = y - (text_height / 1.5)
            draw.text(
                (coord_x, coord_y),
                text_string,
                font=font,
                fill="#000"
            )
            # If text on second card but not last page
            if text_number % 2 == 1 and text_number != len(text) - 1:
                pages.append({"type": "image", "data": page})

    pages.append({"type": "image", "data": page})
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
    return "{} - {}".format(
        task["type"].replace("_", " "),
        task["paper_size"]
    )


def valid_options():
    """Provide dictionary of all valid parameters.

    This excludes the header text parameter.

    Returns:
        All valid options. (dict)
    """
    return {
        "type": [
            "small_numbers", "large_numbers", "fractions", "maori_numbers",
            "words", "letters", "maori_colours", "riding_hood", "butterfly"
        ],
        "paper_size": ["a4", "letter"],
    }
