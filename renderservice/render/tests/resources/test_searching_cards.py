import itertools
from render.daemon.ResourceGenerator import TaskError
from render.tests.resources.BaseResourceTest import BaseResourceTest


class SearchingCardsResourceTest(BaseResourceTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module = "searching_cards"
        self.BASE_URL = "resources/searching-cards.html"
        self.TASK_TEMPLATE = {
            "resource_slug": "searching-cards",
            "resource_name": "Searching Cards",
            "resource_view": "searching_cards",
            "url": None
        }

    def test_searching_cards_resource_generation_valid_configurations(self):
        resource_module = self.load_module()
        valid_options = resource_module.valid_options()
        valid_options["header_text"] = ["", "Example header"]
        valid_options["copies"] = [1]
        valid_option_keys = sorted(valid_options)

        combinations = [
            dict(zip(valid_option_keys, product))
            for product in itertools.product(
                *(valid_options[valid_option_key] for valid_option_key in valid_option_keys))
        ]

        print()
        print("Testing Searching Cards:")
        for combination in combinations:
            print("   - Testing combination: {} ... ".format(combination), end="")
            url = self.BASE_URL + self.query_string(combination)
            task = self.TASK_TEMPLATE.copy()
            task.update(combination)
            task["url"] = url

            filename, pdf = self.generator.generate_resource_pdf(task)
            print("ok")

    def test_searching_cards_resource_generation_missing_number_cards_parameter(self):
        combination = {
            "max_number": "99",
            "help_sheet": True,
            "paper_size": "a4",
            "header_text": "",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        with self.assertRaises(TaskError):
            filename, pdf = self.generator.generate_resource_pdf(task)

    def test_searching_cards_resource_generation_missing_max_number_parameter(self):
        combination = {
            "number_cards": "15",
            "help_sheet": True,
            "paper_size": "a4",
            "header_text": "",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        with self.assertRaises(TaskError):
            filename, pdf = self.generator.generate_resource_pdf(task)

    def test_searching_cards_resource_generation_missing_help_sheet_parameter(self):
        combination = {
            "number_cards": "15",
            "max_number": "99",
            "paper_size": "a4",
            "header_text": "",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        with self.assertRaises(TaskError):
            filename, pdf = self.generator.generate_resource_pdf(task)

    def test_searching_cards_resource_generation_missing_paper_size_parameter(self):
        combination = {
            "number_cards": "15",
            "max_number": "99",
            "help_sheet": True,
            "header_text": "",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        with self.assertRaises(TaskError):
            filename, pdf = self.generator.generate_resource_pdf(task)

    def test_searching_cards_resource_generation_missing_header_text_parameter(self):
        expected_filename = "Searching Cards (15 cards - 0 to 99 - with helper sheet - a4).pdf"
        combination = {
            "number_cards": "15",
            "max_number": "99",
            "help_sheet": True,
            "paper_size": "a4",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        filename, pdf = self.generator.generate_resource_pdf(task)
        self.assertEqual(filename, expected_filename)
