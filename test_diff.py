import unittest
from designite_diff import process, _verify
import os

class Designite_diff_tests(unittest.TestCase):
    def test_invalid_path(self):
        self.assertRaises(ValueError, _verify, 'dummypath1')

    def test_valid_path(self):
        exp_path = os.path.abspath('test_files')
        self.assertEqual(_verify('test_files'), exp_path)

    # both folders are identical
    def test_case1(self):
        self.assertTrue(process('test_files/case1/1', 'test_files/case1/2'))

    # folder 1 has one less arch smell
    def test_case2(self):
        self.assertFalse(process('test_files/case2/1', 'test_files/case2/2'))

    # folder 2 has one arch smell that has shuffled class names in cause
    def test_case3(self):
        self.assertTrue(process('test_files/case3/1', 'test_files/case3/2'))

    # folder 1 has one less design smell and folder 2 has three design smells (different) less
    def test_case4(self):
        self.assertFalse(process('test_files/case4/1', 'test_files/case4/2'))

    # folder 1 has one less impl smell and folder 2 has two impl smells (different) less
    def test_case5(self):
        self.assertFalse(process('test_files/case5/1', 'test_files/case5/2'))