import unittest

def load_tests():
    suite = unittest.TestSuite()
    for all_test_suite in unittest.defaultTestLoader.discover('.', pattern='*Test.py'):
	print all_test_suite
        for test_suite in all_test_suite:
	    print all_test_suite
            suite.addTests(test_suite)
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run (load_tests())
