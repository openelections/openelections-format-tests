import csv
from format_tests import format_tests
import glob
import os
import unittest


class FileFormatTests(unittest.TestCase):
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    def test_format(self):
        for csv_file in FileFormatTests.__get_csv_files():
            short_path = os.path.relpath(csv_file, start=FileFormatTests.root_path)

            tests = set()

            header_tests = {
                format_tests.EmptyHeaders(),
                format_tests.LowercaseHeaders(),
                format_tests.UnknownHeaders(),
            }
            tests.update(header_tests)

            tests.add(format_tests.ConsecutiveSpaces())
            tests.add(format_tests.EmptyRows())
            tests.add(format_tests.LeadingAndTrailingSpaces())
            tests.add(format_tests.PrematureLineBreaks())

            with self.subTest(msg=f"{short_path}"):
                with open(csv_file, "r") as csv_data:
                    reader = csv.reader(csv_data)
                    headers = next(reader)

                    tests.add(format_tests.InconsistentNumberOfColumns(headers))

                    for test in tests:
                        test.test(headers)

                    row_tests = tests - header_tests
                    for row in reader:
                        for test in row_tests:
                            test.current_row = reader.line_num
                            test.test(row)

                max_examples = 10
                passed = True
                message = f"\n\n{short_path}"
                for test in tests:
                    if not test.passed:
                        passed = False
                        message += f"\n\n* {test.get_failure_message(max_examples)}"

                self.assertTrue(passed, message)

    @staticmethod
    def __get_csv_files():
        data_folders = glob.glob(os.path.join(FileFormatTests.root_path, "[0-9]" * 4))
        for data_folder in data_folders:
            for root, dirs, files in os.walk(data_folder):
                for file in files:
                    if file.lower().endswith(".csv"):
                        yield os.path.join(root, file)
