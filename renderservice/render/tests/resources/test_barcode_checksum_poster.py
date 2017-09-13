import itertools
from render.daemon.ResourceGenerator import TaskError
from render.tests.resources.BaseResourceTest import BaseResourceTest


class BarcodeChecksumPosterResourceTest(BaseResourceTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module = "barcode_checksum_poster"
        self.BASE_URL = "resources/barcode-checksum-poster.html"
        self.TASK_TEMPLATE = {
            "resource_slug": "barcode-checksum-poster",
            "resource_name": "Barcode Checksum Poster",
            "resource_view": "barcode_checksum_poster",
            "url": None
        }

    def test_barcode_checksum_poster_resource_generation_valid_configurations(self):
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
        print("Testing Barcode Checksum Poster:")
        for combination in combinations:
            print("   - Testing combination: {} ... ".format(combination), end="")
            url = self.BASE_URL + self.query_string(combination)
            task = self.TASK_TEMPLATE.copy()
            task.update(combination)
            task["url"] = url

            filename, pdf = self.generator.generate_resource_pdf(task)
            print("ok")

    def test_barcode_checksum_poster_resource_generation_missing_barcode_length_parameter(self):
        combination = {
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

    def test_barcode_checksum_poster_resource_generation_missing_paper_size_parameter(self):
        combination = {
            "barcode_length": "12",
            "header_text": "",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        with self.assertRaises(TaskError):
            filename, pdf = self.generator.generate_resource_pdf(task)

    def test_barcode_checksum_poster_resource_generation_missing_header_text_parameter(self):
        expected_filename = "Barcode Checksum Poster (12 digits - a4).pdf"
        combination = {
            "barcode_length": "12",
            "paper_size": "a4",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        filename, pdf = self.generator.generate_resource_pdf(task)
        self.assertEqual(filename, expected_filename)
