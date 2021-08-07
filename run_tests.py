import argparse
from format_tests.test_format import FileFormatTests
import unittest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root_path", type=str, help="the absolute path to the repository containing files to test")
    args = parser.parse_args()

    FileFormatTests.root_path = args.root_path
    test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(FileFormatTests)
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)

    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)
