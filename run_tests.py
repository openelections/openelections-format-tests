import argparse
from format_tests.test_format import FileFormatTests, TestCase
import unittest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root_path", type=str, help="the absolute path to the repository containing files to test")
    parser.add_argument("--log-file", type=str, help="the absolute path to a file that the full failure messages will "
                                                     "be written to")
    args = parser.parse_args()

    TestCase.root_path = args.root_path
    TestCase.log_file = args.log_file

    test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(FileFormatTests)
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)

    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)
