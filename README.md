[![Build Status](https://github.com/openelections/openelections-format-tests/actions/workflows/unit_tests.yml/badge.svg?branch=master)](https://github.com/openelections/openelections-format-tests/actions/workflows/unit_tests.yml?query=branch%3Amaster)

# OpenElections Data Format Tests (DEPRECATED)

**These tests have been incorporated into the [data tests](https://github.com/openelections/openelections-data-tests).**

A collection of tests to validate the format of OpenElections data files.

## Usage
```
usage: run_tests.py [-h] [--group-failures] [--log-file LOG_FILE] [--max-examples N] root_path

positional arguments:
  root_path            the absolute path to the repository containing files to test

optional arguments:
  -h, --help           show this help message and exit
  --group-failures     group the failures by year in the console output using the GitHub Actions group and endgroup workflow commands
  --log-file LOG_FILE  the absolute path to a file that the full failure messages will be written to
  --max-examples N     the maximum number of failing rows to print to the console. If a negative value is provided, all failures will be printed.
```
The data are expected to be contained in CSV files that reside under
directories named by the corresponding election years.  For example,

```
<data repository>
|
|-- 2000
|   |-- a.csv
|   |-- b.csv
|-- 2001
    |-- counties
        |-- c.csv
        |-- d.csv
        |-- e.csv
```
