import argparse
from format_tests.test_format import FileFormatTests, TestCase
import unittest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root_path", type=str, help="the absolute path to the repository containing files to test")
    parser.add_argument("--log-file", type=str, help="the absolute path to a file that the full failure messages will "
                                                     "be written to")
    parser.add_argument("--max-examples", type=int, default=10, metavar="N",
                        help="the maximum number of failing rows to print to the console. If a negative value is "
                             "provided, all failures will be printed.")
    args = parser.parse_args()

    TestCase.root_path = args.root_path
    TestCase.log_file = args.log_file
    TestCase.max_examples = args.max_examples

    test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(FileFormatTests)
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)

    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)
