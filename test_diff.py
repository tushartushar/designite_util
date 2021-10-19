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
        is_same, a_new_smells, a_removed_smells, a_modified_smells, d_new_smells, d_removed_smells, d_modified_smells, *_ = process(
            'test_files/case4/1', 'test_files/case4/2')
        self.assertFalse(is_same)
        self.assertEqual(len(d_new_smells), 3)
        self.assertEqual(len(d_removed_smells), 1)
        self.assertEqual(len(d_modified_smells), 0)

    # folder 1 has one less impl smell and folder 2 has two impl smells (different) less
    def test_case5(self):
        is_same, a_new_smells, a_removed_smells, a_modified_smells, d_new_smells, d_removed_smells, d_modified_smells, i_new_smells, i_removed_smells, i_modified_smells = process(
            'test_files/case5/1', 'test_files/case5/2')
        self.assertFalse(is_same)
        self.assertEqual(len(i_new_smells), 2)
        self.assertEqual(len(i_removed_smells), 1)
        self.assertEqual(len(i_modified_smells), 0)

    # folder 1 has two arch smells (cyclic dep and feature conc modified)
    def test_case8(self):
        is_same, a_new_smells, a_removed_smells, a_modified_smells, *_ = process('test_files/case8/1',
                                                                                 'test_files/case8/2')
        self.assertEqual(a_modified_smells[0].before_metric, 0.33)
        self.assertEqual(a_modified_smells[0].after_metric, 0.38)
        self.assertEqual(a_modified_smells[0].change_in_metric, 0.05)
        self.assertEqual(a_modified_smells[1].before_metric, 4)
        self.assertEqual(a_modified_smells[1].after_metric, 3)
        self.assertEqual(a_modified_smells[1].change_in_metric, 1)

    # cyclic hierarchy (changed target class), cyclically-dependent mod (2 instead of 3 types in cycle), hub-mod (one less incoming dep), insuff mod (26 instead of 23 methods)
    def test_case9(self):
        is_same, a_new_smells, a_removed_smells, a_modified_smells, d_new_smells, d_removed_smells, d_modified_smells, *_ = process(
            'test_files/case9/1', 'test_files/case9/2')
        self.assertEqual(d_modified_smells[0].before_metric, 3)
        self.assertEqual(d_modified_smells[0].after_metric, 2)
        self.assertEqual(d_modified_smells[0].change_in_metric, 1)
        self.assertEqual(d_modified_smells[1].before_metric, 23)
        self.assertEqual(d_modified_smells[1].after_metric, 26)
        self.assertEqual(d_modified_smells[1].change_in_metric, 3)
        self.assertEqual(d_modified_smells[2].before_metric, 1)
        self.assertEqual(d_modified_smells[2].after_metric, 1)
        self.assertEqual(d_modified_smells[2].change_in_metric, 2)
        self.assertEqual(d_modified_smells[3].before_metric, 50)
        self.assertEqual(d_modified_smells[3].after_metric, 49)
        self.assertEqual(d_modified_smells[3].change_in_metric, 1)

    # long id(31->35), magic no (16->18), and complex cond (3 conditions -> 2)
    def test_case10(self):
        is_same, a_new_smells, a_removed_smells, a_modified_smells, d_new_smells, d_removed_smells, \
        d_modified_smells, i_new_smells, i_removed_smells, i_modified_smells = process(
            'test_files/case10/1', 'test_files/case10/2')
        self.assertEqual(i_modified_smells[0].before_metric, 31)
        self.assertEqual(i_modified_smells[0].after_metric, 35)
        self.assertEqual(i_modified_smells[0].change_in_metric, 4)
        self.assertEqual(i_modified_smells[1].before_metric, 16)
        self.assertEqual(i_modified_smells[1].after_metric, 18)
        self.assertEqual(i_modified_smells[1].change_in_metric, 2)
        self.assertEqual(i_modified_smells[2].before_metric, 3)
        self.assertEqual(i_modified_smells[2].after_metric, 2)
        self.assertEqual(i_modified_smells[2].change_in_metric, -1)

