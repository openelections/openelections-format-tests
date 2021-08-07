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
            tests = []

            with self.subTest(msg=f"{short_path}"):
                with open(csv_file, "r") as csv_data:
                    reader = csv.reader(csv_data)
                    headers = next(reader)

                    header_tests = [
                        format_tests.EmptyHeaders(),
                        format_tests.LowercaseHeaders(),
                        format_tests.UnknownHeaders(),
                    ]
                    tests.extend(header_tests)

                    row_tests = [
                        format_tests.ConsecutiveSpaces(),
                        format_tests.EmptyRows(),
                        format_tests.InconsistentNumberOfColumns(headers),
                        format_tests.LeadingAndTrailingSpaces(),
                        format_tests.PrematureLineBreaks(),
                    ]
                    tests.extend(row_tests)

                    for test in header_tests:
                        test.test(headers)

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
