import csv
import os
import re
import subprocess
import tempfile
import unittest

from format_tests import format_tests


class ConsecutiveSpacesTest(unittest.TestCase):
    def test_row(self):
        format_test = format_tests.ConsecutiveSpaces()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        rows = [
            ["a", "b  c", "d"],
            ["a", "  b", "d"],
            ["a", "b", "c"],
            ["a", "b  ", "d"],
            ["a", "b \t", "d"],
            ["a", "b \n", "d"],
        ]

        format_test = format_tests.ConsecutiveSpaces()
        for row in rows:
            format_test.test(row)
        self.assertFalse(format_test.passed)

        failure_message = format_test.get_failure_message()
        self.assertRegex(failure_message, "5 rows.*consecutive whitespace")
        self.assertRegex(failure_message, f"Row 1.*" + re.escape(f"{rows[0]}"))
        self.assertRegex(failure_message, f"Row 2.*" + re.escape(f"{rows[1]}"))
        self.assertNotRegex(failure_message, "Row 3.*")
        self.assertRegex(failure_message, f"Row 4.*" + re.escape(f"{rows[3]}"))
        self.assertRegex(failure_message, f"Row 5.*" + re.escape(f"{rows[4]}"))
        self.assertRegex(failure_message, f"Row 6.*" + re.escape(f"{rows[5]}"))


class EmptyHeadersTest(unittest.TestCase):
    def test_headers(self):
        format_test = format_tests.EmptyHeaders()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        header = ["a", "", "c"]
        format_test = format_tests.EmptyHeaders()
        format_test.test(header)
        self.assertFalse(format_test.passed)

        failure_message = format_test.get_failure_message()
        self.assertRegex(failure_message, re.escape(f"{header}") + ".*empty entries")


class EmptyRowsTest(unittest.TestCase):
    def test_row(self):
        format_test = format_tests.EmptyRows()
        format_test.test(["a", "b", ""])
        self.assertTrue(format_test.passed)

        rows = [
            ["", "", ""],
            ["a", "b", ""],
            [" ", "\t", "\n"]
        ]

        format_test = format_tests.EmptyRows()
        for row in rows:
            format_test.test(row)
        self.assertFalse(format_test.passed)

        failure_message = format_test.get_failure_message()
        self.assertRegex(failure_message, "2 empty rows")


class InconsistentNumberOfColumnsTest(unittest.TestCase):
    def test_row(self):
        headers = ["a", "b", "c"]

        format_test = format_tests.InconsistentNumberOfColumns(headers)
        format_test.test(["d", "e", ""])
        self.assertTrue(format_test.passed)

        rows = [
            ["d", "e"],
            ["d", "e", ""],
            ["d", "e", "f", "g"],
            ["d", "e", ""],
        ]

        format_test = format_tests.InconsistentNumberOfColumns(headers)
        for row in rows:
            format_test.test(row)
        self.assertFalse(format_test.passed)

        failure_message = format_test.get_failure_message()
        self.assertRegex(failure_message, "2 rows.*inconsistent number of columns")
        self.assertRegex(failure_message, f"Row 1.*" + re.escape(f"{rows[0]}"))
        self.assertNotRegex(failure_message, "Row 2.*")
        self.assertRegex(failure_message, f"Row 3.*" + re.escape(f"{rows[2]}"))
        self.assertNotRegex(failure_message, "Row 4.*")


class LeadingAndTrailingSpacesTest(unittest.TestCase):
    def test_row(self):
        format_test = format_tests.LeadingAndTrailingSpaces()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        good_value = "b"
        bad_values = [" b", "b ", "\tb", "b\n"]
        for bad_value in bad_values:
            format_test = format_tests.LeadingAndTrailingSpaces()
            format_test.test(["a", bad_value, "c"])
            format_test.test(["a", good_value, "c"])
            self.assertFalse(format_test.passed)


class LowercaseHeadersTest(unittest.TestCase):
    def test_headers(self):
        format_test = format_tests.LowercaseHeaders()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        format_test = format_tests.LowercaseHeaders()
        format_test.test(["a", "B", "c"])
        self.assertFalse(format_test.passed)

        format_test = format_tests.LowercaseHeaders()
        format_test.test(["A", "B", "c"])
        self.assertFalse(format_test.passed)


class NonIntegerVotesTest(unittest.TestCase):
    def test_headers(self):
        format_test = format_tests.NonIntegerVotes(["a", "b", "c"])
        format_test.test(["a", "1.2", "c"])
        self.assertTrue(format_test.passed)

        format_test = format_tests.NonIntegerVotes(["a", "Percentage", "c"])
        format_test.test(["a", "1.2", "c"])
        self.assertTrue(format_test.passed)

        good_values = ["*", "2", "2.0", "-2", "-2.0"]
        format_test = format_tests.NonIntegerVotes(["a", "votes", "c"])
        for value in good_values:
            format_test.test(["a", value, "c"])
            self.assertTrue(format_test.passed)

        bad_values = ["1.2", "-1.2", "0.01"]
        vote_columns = {"absentee", "early_voting", "election_day", "mail", "provisional", "votes"}
        for column in vote_columns:
            for value in bad_values:
                format_test = format_tests.NonIntegerVotes(["a", "votes ", column, "c"])
                format_test.test(["a", 1, value, "c"])
                self.assertFalse(format_test.passed)


class PrematureLineBreaks(unittest.TestCase):
    def test_row(self):
        format_test = format_tests.PrematureLineBreaks()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        format_test = format_tests.PrematureLineBreaks()
        format_test.test(["a", "b\nc", "d"])
        format_test.test(["a", "b", "c"])
        self.assertFalse(format_test.passed)


class TabCharacters(unittest.TestCase):
    def test_row(self):
        format_test = format_tests.TabCharacters()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        format_test = format_tests.TabCharacters()
        format_test.test(["a", "b\tc", "d"])
        format_test.test(["a", "b", "c"])
        self.assertFalse(format_test.passed)


class UnknownHeadersTest(unittest.TestCase):
    def test_headers(self):
        format_test = format_tests.UnknownHeaders()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        format_test = format_tests.UnknownHeaders()
        format_test.test(["a", "UnkNowN", "c"])
        self.assertFalse(format_test.passed)


class RunTestsTest(unittest.TestCase):
    bad_data_dir = None
    bad_rows = [
        ["County", "unknown", "absentee", "votes", ""],  # Lowercase, unknown, and empty headers
        ["", "", "", "", ""],  # Empty rows
        ["a", "b  c", "1", "2", "3"],  # Consecutive whitespace
        ["a", "b", "c", "1", "2", "3"],  # Inconsistent number of columns
        ["a", "b", "1", "2.5", "3"],  # Non-integer votes
        [" a", "b", "1", "2", "3"],  # Leading whitespace
        ["a ", "b", "1", "2", "3"],  # Trailing whitespace
        ["a", "b", "1\n2", "2", "3"],  # Premature linebreak
        ["a", "b", "1\t2", "2", "3"],  # Tab
        ["a", "b", "1", "2", "3"],  # No errors
    ]
    good_data_dir = None
    good_rows = [
        ["county", "precinct", "absentee", "votes"],
        ["a", "b", "1", "2"],
        ["c", "d", "2", "3"],
    ]
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    @staticmethod
    def create_data(root_path, year, rows):
        year_dir = os.path.join(root_path, year)
        os.mkdir(year_dir)
        _, csv_file_path = tempfile.mkstemp(suffix=".csv", dir=year_dir, text=True)
        with open(csv_file_path, "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

    @classmethod
    def setUpClass(cls):
        cls.bad_data_dir = tempfile.TemporaryDirectory()
        RunTestsTest.create_data(cls.bad_data_dir.name, "2020", cls.bad_rows)

        cls.good_data_dir = tempfile.TemporaryDirectory()
        RunTestsTest.create_data(cls.good_data_dir.name, "2020", cls.good_rows)

    def setUp(self):
        self.log_file = tempfile.NamedTemporaryFile(dir=self.bad_data_dir.name)

    def run_test(self, root_path):
        command = ["python", os.path.join(RunTestsTest.root_path, "run_tests.py"),
                   f"--log-file={self.log_file.name}", root_path]
        completed_process = subprocess.run(command, capture_output=True)
        return completed_process.returncode

    def test_failure(self):
        self.assertEqual(1, self.run_test(self.bad_data_dir.name))

        with open(self.log_file.name, "r") as log_file:
            log_file_contents = "\n".join(log_file.readlines())

        self.assertRegex(log_file_contents, "Header.*" + re.escape(f"{self.bad_rows[0]}") + ".*lowercase")
        self.assertRegex(log_file_contents, "Header.*" + re.escape(f"{self.bad_rows[0]}") + ".*unknown")
        self.assertRegex(log_file_contents, "Header.*" + re.escape(f"{self.bad_rows[0]}") + ".*empty")
        self.assertRegex(log_file_contents, "1 empty rows")
        self.assertRegex(log_file_contents, "1 rows.*consecutive whitespace")
        self.assertRegex(log_file_contents, "1 rows.*inconsistent number of columns")
        self.assertRegex(log_file_contents, "1 rows.*integers")
        self.assertRegex(log_file_contents, "2 rows.*leading or trailing whitespace")
        self.assertRegex(log_file_contents, "1 rows.*newline characters")
        self.assertRegex(log_file_contents, "1 rows.*tab characters")
        self.assertNotRegex(log_file_contents, re.escape(f"{self.bad_rows[-1]}"))

    def test_success(self):
        self.assertEqual(0, self.run_test(self.good_data_dir.name))
