from designiteutil.diff import Diff
from designiteutil.postprocessor import _get_impl_smells_list, _get_impl_smells_list_dpy


class DiffImplDJ(Diff):
    def diff(self, path1, path2):
        impl_smell_list1 = _get_impl_smells_list(path1)
        impl_smell_list2 = _get_impl_smells_list(path2)
        return self.diff_impl(impl_smell_list1, impl_smell_list2)


class DiffImplDpy(Diff):
    def diff(self, path1, path2):
        impl_smell_list1 = _get_impl_smells_list_dpy(path1)
        # print(f'total impl_smells1: {len(impl_smell_list1)}')
        impl_smell_list2 = _get_impl_smells_list_dpy(path2)
        # print(f'total impl_smells2: {len(impl_smell_list2)}')
        return self.diff_impl(impl_smell_list1, impl_smell_list2)
