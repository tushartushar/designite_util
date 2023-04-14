# This utility computes the 'diff' between two output folders generated by DesigniteJava.
import datetime
import sys
import os
import time

from src.postprocessor import _get_arch_smells_list, _get_design_smells_list, _get_impl_smells_list

CAUSE_STATIC_TEXT = 'The tool detected the smell in this component because this component participates in a cyclic dependency. The participating components in the cycle are:'
CAUSE_STATIC_TEXT_DESIGN = 'The tool detected the smell in this class because this class participates in a cyclic dependency. The participating classes in the cycle are: '


def _verify(folder_path):
    path = os.path.abspath(folder_path)
    if os.path.exists(path):
        return path
    raise ValueError("The provided path does not exist: " + str(path))


def common_substring_from_start(str_a, str_b):
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


def is_cause_match(cause1, cause2, static_text=CAUSE_STATIC_TEXT):
    common_str = common_substring_from_start(cause1, cause2)
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


def print_smells(smell_list, msg):
    print(msg)
    for smell in smell_list:
        print('\t' + str(smell))


# If combo of smell name, project name, and package name is present in 1 but not in 2 -> Removed
# If the combo is present in 2 but not in 1 -> New
#  Otherwise, it is modified
def diff_detailed(not_matched_list1, not_matched_list2, smell_text):
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
    print_smells(new_smells, f'New {smell_text} smells:')
    print_smells(removed_smells, f'Removed {smell_text} smells:')
    print_smells(modified_smells, f'Modified {smell_text} smells:')
    return new_smells, removed_smells, modified_smells


def _build_dict_arch(arch_smell_list):
    arch_smells_first = dict()
    for smell in arch_smell_list:
        if smell.smell_name not in arch_smells_first:
            arch_smells_first[smell.smell_name] = dict()
        second_level_key = smell.project_name + smell.package_name
        if second_level_key not in arch_smells_first[smell.smell_name]:
            arch_smells_first[smell.smell_name][second_level_key] = list()
        arch_smells_first[smell.smell_name][second_level_key].append(smell)
    return arch_smells_first

def _build_dict_design(design_smell_list):
    design_smells_first = dict()
    for smell in design_smell_list:
        if smell.smell_name not in design_smells_first:
            design_smells_first[smell.smell_name] = dict()
        second_level_key = smell.project_name + smell.package_name + smell.type_name
        if second_level_key not in design_smells_first[smell.smell_name]:
            design_smells_first[smell.smell_name][second_level_key] = list()
        design_smells_first[smell.smell_name][second_level_key].append(smell)
    return design_smells_first

def _build_dict_impl(impl_smell_list):
    impl_smells_first = dict()
    for smell in impl_smell_list:
        if smell.smell_name not in impl_smells_first:
            impl_smells_first[smell.smell_name] = dict()
        second_level_key = smell.project_name + smell.package_name + smell.type_name + smell.method_name + smell.cause
        if second_level_key not in impl_smells_first[smell.smell_name]:
            impl_smells_first[smell.smell_name][second_level_key] = list()
        impl_smells_first[smell.smell_name][second_level_key].append(smell)
    return impl_smells_first

def diff_arch(path1, path2):
    arch_smell_list1 = _get_arch_smells_list(path1)
    arch_smell_list2 = _get_arch_smells_list(path2)
    # arch_smells1 = _build_dict_arch(arch_smell_list1)
    arch_smells2 = _build_dict_arch(arch_smell_list2)
    for smell in arch_smell_list1:
        # filtered_list = filter(lambda item:
        #                        item.smell_name == smell.smell_name and
        #                        item.project_name == smell.project_name and
        #                        item.package_name == smell.package_name,
        #                        arch_smell_list2)
        if smell.smell_name in arch_smells2:
            filtered_list = arch_smells2[smell.smell_name][smell.project_name+smell.package_name] if smell.project_name+smell.package_name in arch_smells2[smell.smell_name] else list()
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
                if is_cause_match(smell.cause, filtered_item.cause):
                    smell.matched = True
                    filtered_item.matched = True
                    break
    not_matched_list1 = list(filter(lambda item:
                                    item.matched is False, arch_smell_list1))
    # print_smells(not_matched_list1, f'Different architecture smells: {path1}')
    not_matched_list2 = list(filter(lambda item:
                                    item.matched is False, arch_smell_list2))
    # print_smells(not_matched_list2, f'Different architecture smells: {path2}')
    new_smells, removed_smells, modified_smells = diff_detailed(not_matched_list1, not_matched_list2,
                                                                'Architecture')
    is_same = True if len(new_smells) == 0 and \
                      len(removed_smells) == 0 and \
                      len(modified_smells) == 0 else False
    return is_same, new_smells, removed_smells, modified_smells


def diff_design(path1, path2):
    design_smell_list1 = _get_design_smells_list(path1)
    design_smell_list2 = _get_design_smells_list(path2)
    design_smells2 = _build_dict_design(design_smell_list2)
    for smell in design_smell_list1:
        # filtered_list = filter(lambda item:
        #                        item.smell_name == smell.smell_name and
        #                        item.project_name == smell.project_name and
        #                        item.package_name == smell.package_name and
        #                        item.type_name == smell.type_name,
        #                        design_smell_list2)
        if smell.smell_name in design_smells2:
            filtered_list = design_smells2[smell.smell_name][smell.project_name + smell.package_name + smell.type_name] if smell.project_name + smell.package_name + smell.type_name in design_smells2[smell.smell_name] else list()
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
                if is_cause_match(smell.cause, filtered_item.cause, CAUSE_STATIC_TEXT_DESIGN):
                    smell.matched = True
                    filtered_item.matched = True
                    break
    not_matched_list1 = list(filter(lambda item:
                                    item.matched is False, design_smell_list1))
    # print_smells(not_matched_list1, f'Different design smells: {path1}')
    not_matched_list2 = list(filter(lambda item:
                                    item.matched is False, design_smell_list2))
    # print_smells(not_matched_list2, f'Different design smells: {path2}')
    new_smells, removed_smells, modified_smells = diff_detailed(not_matched_list1, not_matched_list2, 'Design')
    is_same = True if len(new_smells) == 0 and \
                      len(removed_smells) == 0 and \
                      len(modified_smells) == 0 else False
    return is_same, new_smells, removed_smells, modified_smells


def diff_impl(path1, path2):
    impl_smell_list1 = _get_impl_smells_list(path1)
    impl_smell_list2 = _get_impl_smells_list(path2)
    impl_smells2 = _build_dict_impl(impl_smell_list2)
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
        key = smell.project_name + smell.package_name + smell.type_name +smell.method_name + smell.cause
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
    new_smells, removed_smells, modified_smells = diff_detailed(not_matched_list1, not_matched_list2,
                                                                'Implementation')
    is_same = True if len(new_smells) == 0 and \
                      len(removed_smells) == 0 and \
                      len(modified_smells) == 0 else False
    return is_same, new_smells, removed_smells, modified_smells

def time_it(msg):
    print(str(datetime.datetime.now()) + ' - ' + msg)

# Accepts two folder paths (assumes that both the folders are generated by DesigniteJava)
# Returns 1: whether both the folders are same from detected smells perspective
# 2 and 3: list of different arch smells in folder 1 and 2 respectively
# 4 and 5: list of different design smells in folder 1 and 2 respectively
# 6 and 7: list of different impl smells in folder 1 and 2 respectively
def process(path1, path2):
    path1 = _verify(path1)
    path2 = _verify(path2)
    start_time = time.time()
    is_same_arch, arch_new_smells, arch_removed_smells, arch_modified_smells = diff_arch(path1, path2)
    is_same_design, design_new_smells, design_removed_smells, design_modified_smells = diff_design(path1, path2)
    is_same_impl, impl_new_smells, impl_removed_smells, impl_modified_smells = diff_impl(path1, path2)
    is_same = is_same_arch and is_same_design and is_same_impl
    print('is_same: ' + str(is_same))
    print('Elapsed time: ' + str(time.time() - start_time))
    return is_same, arch_new_smells, arch_removed_smells, arch_modified_smells, design_new_smells, design_removed_smells, \
           design_modified_smells, impl_new_smells, impl_removed_smells, impl_modified_smells


if __name__ == '__main__':
    if len(sys.argv) > 2:
        # order the filenames so we have consistent output irrespective of the order of the parameters
        # since the output is symmetric anyways
        files = sys.argv[1:3]
        # if sys.argv[1] > sys.argv[2]:
        #     files.reverse()  # i hate that these functions modify rather than return a new list

        process(files[0], files[1])
    else:
        print('Argument error\nUsage:\ndesignite_diff <path of first output folder> <path of second output folder>')
