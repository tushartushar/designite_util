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
        is_same, new_smells, removed_smells, modified_smells, *_ = process('test_files/case1/1', 'test_files/case1/2')
        self.assertTrue(is_same)
        self.assertEqual(len(new_smells), 0)
        self.assertEqual(len(removed_smells), 0)
        self.assertEqual(len(modified_smells), 0)

    # folder 1 has one less arch smell
    def test_case2(self):
        is_same, new_smells, removed_smells, modified_smells, *_ = process('test_files/case2/1', 'test_files/case2/2')
        self.assertFalse(is_same)
        self.assertEqual(len(new_smells), 0)
        self.assertEqual(len(removed_smells), 1)
        self.assertEqual(len(modified_smells), 0)

    # folder 1 has more less arch smell
    def test_case6(self):
        is_same, new_smells, removed_smells, modified_smells, *_ = process('test_files/case6/1', 'test_files/case6/2')
        self.assertFalse(is_same)
        self.assertEqual(len(new_smells), 1)
        self.assertEqual(len(removed_smells), 0)
        self.assertEqual(len(modified_smells), 0)

    # folder 1 has one modified (in cause) arch smell
    def test_case7(self):
        is_same, new_smells, removed_smells, modified_smells, *_ = process('test_files/case7/1', 'test_files/case7/2')
        self.assertFalse(is_same)
        self.assertEqual(len(new_smells), 0)
        self.assertEqual(len(removed_smells), 0)
        self.assertEqual(len(modified_smells), 1)

    # folder 2 has one arch smell that has shuffled class names in cause
    def test_case3(self):
        is_same, new_smells, removed_smells, modified_smells, *_ = process('test_files/case3/1', 'test_files/case3/2')
        self.assertTrue(is_same)
        self.assertEqual(len(new_smells), 0)
        self.assertEqual(len(removed_smells), 0)
        self.assertEqual(len(modified_smells), 0)


    # folder 1 has one less design smell and folder 2 has three design smells (different) less
    def test_case4(self):
        is_same, a_new_smells, a_removed_smells, a_modified_smells, d_new_smells, d_removed_smells, d_modified_smells, *_ = process('test_files/case4/1', 'test_files/case4/2')
        self.assertFalse(is_same)
        self.assertEqual(len(d_new_smells), 3)
        self.assertEqual(len(d_removed_smells), 1)
        self.assertEqual(len(d_modified_smells), 0)

    # folder 1 has one less impl smell and folder 2 has two impl smells (different) less
    def test_case5(self):
        is_same, a_new_smells, a_removed_smells, a_modified_smells, d_new_smells, d_removed_smells, d_modified_smells, i_new_smells, i_removed_smells, i_modified_smells= process('test_files/case5/1', 'test_files/case5/2')
        self.assertFalse(is_same)
        self.assertEqual(len(i_new_smells), 2)
        self.assertEqual(len(i_removed_smells), 1)
        self.assertEqual(len(i_modified_smells), 0)
