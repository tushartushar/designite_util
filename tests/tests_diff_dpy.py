import unittest

from designiteutil.designite_diff import process


class Designite_diff_tests(unittest.TestCase):
    # both folders are identical
    def test_case12(self):
        is_same, new_smells, removed_smells, modified_smells, *_ = process('test_files/case12/1', 'test_files/case12/2', source_tool='dpy')
        self.assertTrue(is_same)
        self.assertEqual(len(new_smells), 0)
        self.assertEqual(len(removed_smells), 0)
        self.assertEqual(len(modified_smells), 0)

    # folder 1 has one less design smell
    def test_case13(self):
        is_same, a_new_smells, a_removed_smells, a_modified_smells, d_new_smells, d_removed_smells, d_modified_smells, *_= process('test_files/case13/1', 'test_files/case13/2', source_tool='dpy')
        self.assertFalse(is_same)
        self.assertEqual(len(d_new_smells), 1)
        self.assertEqual(len(d_removed_smells), 0)
        self.assertEqual(len(d_modified_smells), 0)

    # folder 1 has one more design smell
    def test_case14(self):
        is_same, a_new_smells, a_removed_smells, a_modified_smells, d_new_smells, d_removed_smells, d_modified_smells, *_= process('test_files/case14/1', 'test_files/case14/2', source_tool='dpy')
        self.assertFalse(is_same)
        self.assertEqual(len(d_new_smells), 0)
        self.assertEqual(len(d_removed_smells), 1)
        self.assertEqual(len(d_modified_smells), 0)

    # folder 1 has one less impl smell and folder 2 has two impl smells (different) less
    def test_case15(self):
        is_same, a_new_smells, a_removed_smells, a_modified_smells, d_new_smells, d_removed_smells, d_modified_smells, i_new_smells, i_removed_smells, i_modified_smells = process(
            'test_files/case15/1', 'test_files/case15/2', source_tool='dpy')
        self.assertFalse(is_same)
        self.assertEqual(len(i_new_smells), 1)
        self.assertEqual(len(i_removed_smells), 2)
        self.assertEqual(len(i_modified_smells), 0)