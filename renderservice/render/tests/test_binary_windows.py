import itertools
from render.daemon.ResourceGenerator import TaskError
from render.tests.BaseResourceTest import BaseResourceTest


class BinaryWindowsResourceTest(BaseResourceTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module = "binary_windows"
        self.BASE_URL = "resources/binary-windows.html"
        self.TASK_TEMPLATE = {
            "resource_slug": "binary-windows",
            "resource_name": "Binary Windows",
            "resource_view": "binary_windows",
            "url": None
        }

    def test_binary_windows_resource_generation_valid_configurations(self):
        resource_module = self.load_module()
        valid_options = resource_module.valid_options()
        valid_options["header_text"] = ["", "Example header"]
        valid_options["copies"] = [1, 2]
        valid_option_keys = sorted(valid_options)

        combinations = [
            dict(zip(valid_option_keys, product))
            for product in itertools.product(
                *(valid_options[valid_option_key] for valid_option_key in valid_option_keys))
        ]

        print()
        print("Testing Binary Windows:")
        for combination in combinations:
            print("   - Testing combination: {} ... ".format(combination), end="")
            url = self.BASE_URL + self.query_string(combination)
            task = self.TASK_TEMPLATE.copy()
            task.update(combination)
            task["url"] = url

            filename, pdf = self.generator.generate_resource_pdf(task)
            print("ok")

    def test_binary_windows_resource_generation_missing_dot_count_parameter(self):
        combination = {
            "number_bits": "8",
            "value_type": "binary",
            "paper_size": "a4",
            "header_text": "Example header text",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        with self.assertRaises(TaskError):
            filename, pdf = self.generator.generate_resource_pdf(task)

    def test_binary_windows_resource_generation_missing_number_bits_parameter(self):
        combination = {
            "dot_counts": True,
            "value_type": "binary",
            "paper_size": "a4",
            "header_text": "Example header text",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        with self.assertRaises(TaskError):
            filename, pdf = self.generator.generate_resource_pdf(task)

    def test_binary_windows_resource_generation_missing_value_type_parameter(self):
        combination = {
            "dot_counts": True,
            "number_bits": "8",
            "paper_size": "a4",
            "header_text": "Example header text",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        with self.assertRaises(TaskError):
            filename, pdf = self.generator.generate_resource_pdf(task)

    def test_binary_windows_resource_generation_missing_paper_size_parameter(self):
        combination = {
            "dot_counts": True,
            "number_bits": "8",
            "value_type": "binary",
            "header_text": "Example header text",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        with self.assertRaises(TaskError):
            filename, pdf = self.generator.generate_resource_pdf(task)

    def test_binary_windows_resource_generation_missing_header_text_parameter(self):
        expected_filename = "Binary Windows (8 bits - lightbulb - with dot counts).pdf"
        combination = {
            "dot_counts": True,
            "number_bits": "8",
            "value_type": "lightbulb",
            "paper_size": "a4",
            "copies": 1
        }

        url = self.BASE_URL + self.query_string(combination)
        task = self.TASK_TEMPLATE.copy()
        task.update(combination)
        task["url"] = url

        filename, pdf = self.generator.generate_resource_pdf(task)
        self.assertEqual(filename, expected_filename)
