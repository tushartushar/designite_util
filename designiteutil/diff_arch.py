from designiteutil.diff import Diff
from designiteutil.postprocessor import _get_arch_smells_list


class DiffArchDJ(Diff):
    def diff(self, path1, path2):
        arch_smell_list1 = _get_arch_smells_list(path1)
        arch_smell_list2 = _get_arch_smells_list(path2)
        # arch_smells1 = _build_dict_arch(arch_smell_list1)
        arch_smells2 = self._build_dict_arch(arch_smell_list2)
        for smell in arch_smell_list1:
            # filtered_list = filter(lambda item:
            #                        item.smell_name == smell.smell_name and
            #                        item.project_name == smell.project_name and
            #                        item.package_name == smell.package_name,
            #                        arch_smell_list2)
            if smell.smell_name in arch_smells2:
                filtered_list = arch_smells2[smell.smell_name][
                    smell.project_name + smell.package_name] if smell.project_name + smell.package_name in arch_smells2[
                    smell.smell_name] else list()
            else:
                filtered_list = list()
            for filtered_item in filtered_list:
                if filtered_item.matched:
                    continue
                if filtered_item.cause == smell.cause:
                    smell.matched = True
                    filtered_item.matched = True
                    break
                else:
                    if self.is_cause_match(smell.cause, filtered_item.cause):
                        smell.matched = True
                        filtered_item.matched = True
                        break
        not_matched_list1 = list(filter(lambda item:
                                        item.matched is False, arch_smell_list1))
        # print_smells(not_matched_list1, f'Different architecture smells: {path1}')
        not_matched_list2 = list(filter(lambda item:
                                        item.matched is False, arch_smell_list2))
        # print_smells(not_matched_list2, f'Different architecture smells: {path2}')
        new_smells, removed_smells, modified_smells = self.diff_detailed(not_matched_list1, not_matched_list2,
                                                                         'Architecture')
        is_same = True if len(new_smells) == 0 and \
                          len(removed_smells) == 0 and \
                          len(modified_smells) == 0 else False
        return is_same, new_smells, removed_smells, modified_smells

    def _build_dict_arch(self, arch_smell_list):
        arch_smells_first = dict()
        for smell in arch_smell_list:
            if smell.smell_name not in arch_smells_first:
                arch_smells_first[smell.smell_name] = dict()
            second_level_key = smell.project_name + smell.package_name
            if second_level_key not in arch_smells_first[smell.smell_name]:
                arch_smells_first[smell.smell_name][second_level_key] = list()
            arch_smells_first[smell.smell_name][second_level_key].append(smell)
        return arch_smells_first


class DiffArchDpy(Diff):
    def diff(self, path1, path2):
        return True, [], [], []