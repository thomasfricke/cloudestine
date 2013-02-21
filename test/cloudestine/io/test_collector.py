import unittest2

def load_tests(a,b,v):
    suite = unittest2.TestSuite()
    for all_test_suite in unittest2.defaultTestLoader.discover('..', pattern='f*test.py'):
        print all_test_suite
        
        if all_test_suite:
            for test_suite in all_test_suite:
                suite.addTests(test_suite)
    return suite

if __name__ == '__main__':
    runner = unittest2.runner
    runner.run (load_tests())
