import unittest2


def load_tests(ignored_loader, standard_tests, ignored_start):
    for directory in ['io','crypt']:
        loader=unittest2.TestLoader()
        for all_test_suite in loader.discover(start_dir=directory, 
                                             pattern='*test.py'):
            for test_suite in all_test_suite:
                standard_tests.addTests(test_suite)

    return standard_tests
