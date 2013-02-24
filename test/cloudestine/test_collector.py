import unittest2

def load_tests(loader,standard_tests,start):
    for all_test_suite in loader.discover(start_dir='crypt', 
                                             pattern='*test.py'):
        print all_test_suite
            
        for test_suite in all_test_suite:
            print test_suite
            standard_tests.addTests(test_suite)
    
    return standard_tests

if __name__ == '__main__':
    runner = unittest2.runner
    runner.run (load_tests(start='io'))
