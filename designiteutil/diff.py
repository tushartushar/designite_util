from abc import ABC, abstractmethod


class Diff(ABC):
    @abstractmethod
    def diff(self, path1, path2):
        pass

    # If combo of smell name, project name, and package name is present in 1 but not in 2 -> Removed
    # If the combo is present in 2 but not in 1 -> New
    #  Otherwise, it is modified
    def diff_detailed(self, not_matched_list1, not_matched_list2, smell_text):
        modified_smells = list()
        removed_smells = list()
        for smell in not_matched_list2:
            smell.matched = False
        for smell in not_matched_list1:
            is_present, similar_smell = smell.is_smell_present(not_matched_list2)
            if is_present:
                modified_smells.append(smell)
                smell.populate_diff_metrics(similar_smell)
            else:
                # new_smells.append(smell)
                removed_smells.append(smell)
        new_smells = list(filter(lambda item: item.matched is False, not_matched_list2))
        self.print_smells(new_smells, f'New {smell_text} smells:')
        self.print_smells(removed_smells, f'Removed {smell_text} smells:')
        self.print_smells(modified_smells, f'Modified {smell_text} smells:')
        return new_smells, removed_smells, modified_smells

    def print_smells(self, smell_list, msg):
        print(msg)
        for smell in smell_list:
            print('\t' + str(smell))

    def is_cause_match(self, cause1, cause2):
        common_str = self._common_substring_from_start(cause1, cause2)
        cause1 = cause1.replace(common_str, '').rstrip('.')
        cause2 = cause2.replace(common_str, '').rstrip('.')
        cause1_set = set([x.strip() for x in cause1.split(';')])
        cause2_set = set([x.strip() for x in cause2.split(';')])
        diff1 = cause1_set.difference(cause2_set)
        diff2 = cause2_set.difference(cause1_set)

        if len(diff1) > 0 or len(diff2) > 0:
            return False
        else:
            return True

    def _common_substring_from_start(self, str_a, str_b):
        """ returns the longest common substring from the beginning of str_a and str_b """

        def _iter():
            for a, b in zip(str_a, str_b):
                if a == b:
                    yield a
                    if a == ':' or b == ':':
                        return
                else:
                    return

        return ''.join(_iter())

    def build_dict_design(self, design_smell_list):
        design_smells_first = dict()
        for smell in design_smell_list:
            if smell.smell_name not in design_smells_first:
                design_smells_first[smell.smell_name] = dict()
            second_level_key = smell.project_name + smell.package_name + smell.type_name
            if second_level_key not in design_smells_first[smell.smell_name]:
                design_smells_first[smell.smell_name][second_level_key] = list()
            design_smells_first[smell.smell_name][second_level_key].append(smell)
        return design_smells_first

    def build_dict_impl(self, impl_smell_list):
        impl_smells_first = dict()
        for smell in impl_smell_list:
            if smell.smell_name not in impl_smells_first:
                impl_smells_first[smell.smell_name] = dict()
            second_level_key = smell.project_name + smell.package_name + smell.type_name + smell.method_name + smell.cause
            if second_level_key not in impl_smells_first[smell.smell_name]:
                impl_smells_first[smell.smell_name][second_level_key] = list()
            impl_smells_first[smell.smell_name][second_level_key].append(smell)
        return impl_smells_first

    def diff_impl(self, impl_smell_list1, impl_smell_list2):
        impl_smells2 = self.build_dict_impl(impl_smell_list2)
        for smell in impl_smell_list1:
            # filtered_list = filter(lambda item:
            #                        item.smell_name == smell.smell_name and
            #                        item.project_name == smell.project_name and
            #                        item.package_name == smell.package_name and
            #                        item.type_name == smell.type_name and
            #                        item.method_name == smell.method_name and
            #                        item.cause == smell.cause,
            #                        # Removing the start line no check, it seems unnecessary.
            #                        # and item.m_start_line_no == smell.m_start_line_no,
            #                        impl_smell_list2)
            key = smell.project_name + smell.package_name + smell.type_name + smell.method_name + smell.cause
            if smell.smell_name in impl_smells2:
                filtered_list = impl_smells2[smell.smell_name][key] if key in impl_smells2[smell.smell_name] else list()
            else:
                filtered_list = list()
            for filtered_item in filtered_list:
                if filtered_item.matched:
                    continue
                smell.matched = True
                filtered_item.matched = True
                break

        not_matched_list1 = list(filter(lambda item:
                                        item.matched is False, impl_smell_list1))
        # print_smells(not_matched_list1, f'Different implementation smells: {path1}')
        not_matched_list2 = list(filter(lambda item:
                                        item.matched is False, impl_smell_list2))
        # print_smells(not_matched_list2, f'Different implementation smells: {path2}')
        new_smells, removed_smells, modified_smells = self.diff_detailed(not_matched_list1, not_matched_list2,
                                                                         'Implementation')
        is_same = True if len(new_smells) == 0 and \
                          len(removed_smells) == 0 and \
                          len(modified_smells) == 0 else False
        return is_same, new_smells, removed_smells, modified_smells

    def diff_design(self, design_smell_list1, design_smell_list2):
        design_smells2 = self.build_dict_design(design_smell_list2)
        for smell in design_smell_list1:
            # filtered_list = filter(lambda item:
            #                        item.smell_name == smell.smell_name and
            #                        item.project_name == smell.project_name and
            #                        item.package_name == smell.package_name and
            #                        item.type_name == smell.type_name,
            #                        design_smell_list2)
            if smell.smell_name in design_smells2:
                filtered_list = design_smells2[smell.smell_name][
                    smell.project_name + smell.package_name + smell.type_name] if smell.project_name + smell.package_name + smell.type_name in \
                                                                                  design_smells2[
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
                                        item.matched is False, design_smell_list1))
        # print_smells(not_matched_list1, f'Different design smells: {path1}')
        not_matched_list2 = list(filter(lambda item:
                                        item.matched is False, design_smell_list2))
        # print_smells(not_matched_list2, f'Different design smells: {path2}')
        new_smells, removed_smells, modified_smells = self.diff_detailed(not_matched_list1, not_matched_list2, 'Design')
        is_same = True if len(new_smells) == 0 and \
                          len(removed_smells) == 0 and \
                          len(modified_smells) == 0 else False
        return is_same, new_smells, removed_smells, modified_smells
