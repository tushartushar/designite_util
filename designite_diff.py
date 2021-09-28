# This utility computes the 'diff' between two output folders generated by DesigniteJava.
import sys
import os

from postprocessor import _get_arch_smells_list, _get_design_smells_list, _get_impl_smells_list

CAUSE_STATIC_TEXT = 'The tool detected the smell in this component because this component participates in a cyclic dependency. The participating components in the cycle are:'
CAUSE_STATIC_TEXT_DESIGN = 'The tool detected the smell in this class because this class participates in a cyclic dependency. The participating classes in the cycle are: '


def _verify(folder_path):
    path = os.path.abspath(folder_path)
    if os.path.exists(path):
        return path
    raise ValueError("The provided path does not exist: " + str(path))


def is_cause_match(cause1, cause2, static_text=CAUSE_STATIC_TEXT):
    cause1 = cause1.replace(static_text, '')
    cause2 = cause2.replace(static_text, '')
    cause1_set = set([x.strip() for x in cause1.split(';')])
    cause2_set = set([x.strip() for x in cause2.split(';')])
    if len(cause1_set.difference(cause2_set)) > 0:
        return False
    else:
        return True


def print_smells(smell_list, msg):
    print(msg)
    for smell in smell_list:
        print('\t' + str(smell))


def diff_arch(path1, path2):
    arch_smell_list1 = _get_arch_smells_list(path1)
    arch_smell_list2 = _get_arch_smells_list(path2)
    for smell in arch_smell_list1:
        filtered_list = filter(lambda item:
                               item.smell_name == smell.smell_name and
                               item.project_name == smell.project_name and
                               item.package_name == smell.package_name,
                               arch_smell_list2)
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
                                    item.matched == False, arch_smell_list1))
    print_smells(not_matched_list1, f'Different architecture smells: {path1}')
    not_matched_list2 = list(filter(lambda item:
                                    item.matched == False, arch_smell_list2))
    print_smells(not_matched_list2, f'Different architecture smells: {path2}')
    is_same = True if len(not_matched_list1) == 0 and \
                      len(not_matched_list2) == 0 else False
    return is_same, not_matched_list1, not_matched_list2


def diff_design(path1, path2):
    design_smell_list1 = _get_design_smells_list(path1)
    design_smell_list2 = _get_design_smells_list(path2)
    for smell in design_smell_list1:
        filtered_list = filter(lambda item:
                               item.smell_name == smell.smell_name and
                               item.project_name == smell.project_name and
                               item.package_name == smell.package_name and
                               item.type_name == smell.type_name,
                               design_smell_list2)
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
                                    item.matched == False, design_smell_list1))
    print_smells(not_matched_list1, f'Different design smells: {path1}')
    not_matched_list2 = list(filter(lambda item:
                                    item.matched == False, design_smell_list2))
    print_smells(not_matched_list2, f'Different design smells: {path2}')
    is_same = True if len(not_matched_list1) == 0 and \
                      len(not_matched_list2) == 0 else False
    return is_same, not_matched_list1, not_matched_list2


def diff_impl(path1, path2):
    impl_smell_list1 = _get_impl_smells_list(path1)
    impl_smell_list2 = _get_impl_smells_list(path2)
    for smell in impl_smell_list1:
        filtered_list = filter(lambda item:
                               item.smell_name == smell.smell_name and
                               item.project_name == smell.project_name and
                               item.package_name == smell.package_name and
                               item.type_name == smell.type_name and
                               item.method_name == smell.method_name and
                               item.cause == smell.cause and
                               item.m_start_line_no == smell.m_start_line_no,
                               impl_smell_list2)
        for filtered_item in filtered_list:
            if filtered_item.matched:
                continue
            smell.matched = True
            filtered_item.matched = True
            break

    not_matched_list1 = list(filter(lambda item:
                                    item.matched == False, impl_smell_list1))
    print_smells(not_matched_list1, f'Different implementation smells: {path1}')
    not_matched_list2 = list(filter(lambda item:
                                    item.matched == False, impl_smell_list2))
    print_smells(not_matched_list2, f'Different implementation smells: {path2}')
    is_same = True if len(not_matched_list1) == 0 and \
                      len(not_matched_list2) == 0 else False
    return is_same, not_matched_list1, not_matched_list2

# Accepts two folder paths (assumes that both the folders are generated by DesigniteJava)
# Returns 1: whether both the folders are same from detected smells perspective
# 2 and 3: list of different arch smells in folder 1 and 2 respectively
# 4 and 5: list of different design smells in folder 1 and 2 respectively
# 6 and 7: list of different impl smells in folder 1 and 2 respectively
def process(path1, path2):
    path1 = _verify(path1)
    path2 = _verify(path2)
    is_same_arch, arch_not_matched_list1, arch_not_matched_list2 = diff_arch(path1, path2)
    is_same_design, design_not_matched_list1, design_not_matched_list2 = diff_design(path1, path2)
    is_same_impl, impl_not_matched_list1, impl_not_matched_list2 = diff_impl(path1, path2)
    is_same = is_same_arch and is_same_design and is_same_impl
    print('is_same: ' + str(is_same))
    return is_same, arch_not_matched_list1, arch_not_matched_list2, design_not_matched_list1, design_not_matched_list2, impl_not_matched_list1, impl_not_matched_list2


if __name__ == '__main__':
    if len(sys.argv) > 2:
        # order the filenames so we have consistent output irrespective of the order of the parameters
        # since the output is symmetric anyways
        files = sys.argv[1:3]
        if sys.argv[1] > sys.argv[2]:
            files.reverse() # i hate that these functions modify rather than return a new list

        process(files[0],files[1])
    else:
        print('Argument error\nUsage:\ndesignite_diff <path of first output folder> <path of second output folder>')
