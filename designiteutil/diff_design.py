from designiteutil.diff import Diff
from designiteutil.postprocessor import _get_design_smells_list, _get_design_smells_list_dpy


class DiffDesignDJ(Diff):
    def diff(self, path1, path2):
        design_smell_list1 = _get_design_smells_list(path1)
        design_smell_list2 = _get_design_smells_list(path2)
        return self.diff_design(design_smell_list1, design_smell_list2)


class DiffDesignDpy(Diff):
    def diff(self, path1, path2):
        design_smell_list1 = _get_design_smells_list_dpy(path1)
        design_smell_list2 = _get_design_smells_list_dpy(path2)
        return self.diff_design(design_smell_list1, design_smell_list2)
