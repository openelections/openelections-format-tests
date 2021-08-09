import unittest

from format_tests import format_tests


class ConsecutiveSpacesTest(unittest.TestCase):
    def test_row(self):
        format_test = format_tests.ConsecutiveSpaces()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        bad_values = ["b  c", "  b", "b  ", "b \t", "b \n"]
        for value in bad_values:
            format_test = format_tests.ConsecutiveSpaces()
            format_test.test(["a", value, "d"])
            self.assertFalse(format_test.passed)


class EmptyHeadersTest(unittest.TestCase):
    def test_headers(self):
        format_test = format_tests.EmptyHeaders()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        format_test = format_tests.EmptyHeaders()
        format_test.test(["a", "", "c"])
        self.assertFalse(format_test.passed)

        format_test = format_tests.EmptyHeaders()
        format_test.test(["", "", "c"])
        self.assertFalse(format_test.passed)


class EmptyRowsTest(unittest.TestCase):
    def test_row(self):
        format_test = format_tests.EmptyRows()
        format_test.test(["a", "b", ""])
        self.assertTrue(format_test.passed)

        format_test = format_tests.EmptyRows()
        format_test.test(["", "", ""])
        self.assertFalse(format_test.passed)

        format_test = format_tests.EmptyRows()
        format_test.test([" ", "\t", "\n"])
        self.assertFalse(format_test.passed)


class InconsistentNumberOfColumnsTest(unittest.TestCase):
    def test_row(self):
        headers = ["a", "b", "c"]

        format_test = format_tests.InconsistentNumberOfColumns(headers)
        format_test.test(["d", "e", ""])
        self.assertTrue(format_test.passed)

        format_test = format_tests.InconsistentNumberOfColumns(headers)
        format_test.test(["d", "e"])
        self.assertFalse(format_test.passed)

        format_test = format_tests.InconsistentNumberOfColumns(headers)
        format_test.test(["d", "e", "f", "g"])
        self.assertFalse(format_test.passed)


class LeadingAndTrailingSpacesTest(unittest.TestCase):
    def test_row(self):
        format_test = format_tests.LeadingAndTrailingSpaces()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        bad_values = [" b", "b ", "\tb", "b\n"]
        for value in bad_values:
            format_test = format_tests.LeadingAndTrailingSpaces()
            format_test.test(["a", value, "c"])
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


class PrematureLineBreaks(unittest.TestCase):
    def test_row(self):
        format_test = format_tests.PrematureLineBreaks()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        format_test = format_tests.PrematureLineBreaks()
        format_test.test(["a", "b\nc", "d"])
        self.assertFalse(format_test.passed)


class UnknownHeadersTest(unittest.TestCase):
    def test_headers(self):
        format_test = format_tests.UnknownHeaders()
        format_test.test(["a", "b", "c"])
        self.assertTrue(format_test.passed)

        format_test = format_tests.UnknownHeaders()
        format_test.test(["a", "UnkNowN", "c"])
        self.assertFalse(format_test.passed)
