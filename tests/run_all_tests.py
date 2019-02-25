import os
import unittest


def run_all_tests_in_this_folder():
    loader = unittest.TestLoader()
    cwd = os.getcwd()
    suite = loader.discover(cwd)

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    run_all_tests_in_this_folder()
