import re

from constants import *


class Type:
    def __init__(self, project_name, package_name, type_name, file_path, start_line_no):
        self.project_name = project_name
        self.package_name = package_name
        self.type_name = type_name
        self.file_path = file_path
        self.start_line_no = start_line_no


class Method:
    def __init__(self, project_name, package_name, type_name, method_name, start_line_no):
        self.project_name = project_name
        self.package_name = package_name
        self.type_name = type_name
        self.method_name = method_name
        self.start_line_no = start_line_no


class ImplSmell:
    def __init__(self, project_name, package_name, type_name, method_name, smell_name, cause, line_no):
        self.project_name = project_name.strip('\n')
        self.package_name = package_name
        self.type_name = type_name
        self.method_name = method_name
        self.smell_name = smell_name
        self.cause = cause.strip('\n')
        self.m_start_line_no = line_no.strip('\n')
        self.matched = False
        self.before_metric = 0
        self.after_metric = 0
        self.change_in_metric = 0

    def __str__(self):
        return self.project_name + ', ' + self.package_name + ', ' + self.type_name + ', ' + self.method_name + ', ' + self.smell_name + ', ' + self.cause + ', ' + self.m_start_line_no.strip(
            '\n') + ', ' + str(
            self.before_metric) + ', ' + str(self.after_metric) + ', ' + str(self.change_in_metric)

    def is_smell_present(self, smell_list):
        filtered_list = filter(lambda item:
                               item.smell_name == self.smell_name and
                               item.project_name == self.project_name and
                               item.package_name == self.package_name and
                               item.type_name == self.type_name and
                               item.method_name == self.method_name,
                               smell_list)
        for item in filtered_list:
            if not item.matched:
                item.matched = True
                return True, item
        return False, None

    def populate_diff_metrics(self, similar_smell):
        if self.smell_name == I_COMP_COND:
            stmt1 = self.cause.replace('is complex.', '').strip()
            stmt2 = similar_smell.cause.replace('is complex.', '').strip()
            self.before_metric = stmt2.count('&&') + stmt2.count('||')
            self.after_metric = stmt1.count('&&') + stmt1.count('||')
            self.change_in_metric = self.after_metric - self.before_metric
        elif self.smell_name == I_COMP_MTD or self.smell_name == I_LONG_ID or \
                self.smell_name == I_LONG_STMT:
            # rest of the three smells differ in a metric
            m1 = re.search(r'is (\d+)', self.cause)
            m2 = re.search(r'is (\d+)', similar_smell.cause)
            if m1 and m2:
                no1 = int(m1.group(1))
                no2 = int(m2.group(1))
                self.before_metric = no2
                self.after_metric = no1
                self.change_in_metric = no1 - no2
        elif self.smell_name == I_LONG_PARAM_LIST or \
                self.smell_name == I_LONG_MTD:
            # rest of the three smells differ in a metric
            m1 = re.search(r'has (\d+)', self.cause)
            m2 = re.search(r'has (\d+)', similar_smell.cause)
            if m1 and m2:
                no1 = int(m1.group(1))
                no2 = int(m2.group(1))
                self.before_metric = no2
                self.after_metric = no1
                self.change_in_metric = no1 - no2
        elif self.smell_name == I_MAGIC_NO:
            # rest of the three smells differ in a metric
            m1 = re.search(r': (\d+)', self.cause)
            m2 = re.search(r': (\d+)', similar_smell.cause)
            if m1 and m2:
                no1 = int(m1.group(1))
                no2 = int(m2.group(1))
                self.before_metric = no2
                self.after_metric = no1
                self.change_in_metric = no1 - no2


class DesignSmell:
    def __init__(self, project_name, package_name, type_name, smell_name, cause):
        self.project_name = project_name.strip('\n')
        self.package_name = package_name
        self.type_name = type_name
        self.smell_name = smell_name.strip()
        self.cause = cause.strip('\n')
        self.matched = False
        self.before_metric = 0
        self.after_metric = 0
        self.change_in_metric = 0

    def __str__(self):
        return self.project_name + ', ' + self.package_name + ', ' + self.type_name + ', ' + self.smell_name + ', ' + self.cause + ', ' + str(
            self.before_metric) + ', ' + str(self.after_metric) + ', ' + str(self.change_in_metric)

    def is_smell_present(self, smell_list):
        filtered_list = filter(lambda item:
                               item.smell_name == self.smell_name and
                               item.project_name == self.project_name and
                               item.package_name == self.package_name and
                               item.type_name == self.type_name,
                               smell_list)
        for item in filtered_list:
            if not item.matched:
                item.matched = True
                return True, item
        return False, None

    def populate_diff_metrics(self, similar_smell):
        common_str = common_substring_from_start(self.cause, similar_smell.cause)
        cause1 = self.cause.replace(common_str, '').rstrip('.')
        cause2 = similar_smell.cause.replace(common_str, '').rstrip('.')

        if self.smell_name == D_BRO_MOD or self.smell_name == D_BRO_HIE or self.smell_name == D_CYC_MOD or self.smell_name == D_CYC_HIE or self.smell_name == D_DEF_ENC or self.smell_name == D_FEA_ENV or self.smell_name == D_UNN_ABS or self.smell_name == D_IMP_ABS or self.smell_name == D_MUL_HIE or self.smell_name == D_REB_HIE or self.smell_name == D_WID_HIE:
            cause1_set = set([x.strip() for x in cause1.split(';')])
            cause2_set = set([x.strip() for x in cause2.split(';')])
            diff1 = cause1_set.difference(cause2_set)
            diff2 = cause2_set.difference(cause1_set)
            # this set of smells produce a list of classes and we need to figure out how many classes are different
            # prev metric, new metric, difference
            self.before_metric = len(cause2_set)
            self.after_metric = len(cause1_set)
            self.change_in_metric = len(diff1) + len(diff2)
        elif self.smell_name == D_UXP_ENC or self.smell_name == D_MIS_HIE:
            # these smells report slightly complex cause; need to parse the text with markers
            types1 = cause1.rpartition('in method')[0]
            types2 = cause2.rpartition('in method')[0]
            cause1_set = set([x.strip() for x in types1.split(';')])
            cause2_set = set([x.strip() for x in types2.split(';')])
            diff1 = cause1_set.difference(cause2_set)
            diff2 = cause2_set.difference(cause1_set)

            self.before_metric = len(cause2_set)
            self.after_metric = len(cause1_set)
            self.change_in_metric = len(diff1) + len(diff2)
        elif self.smell_name == D_HUB_MOD:
            # these smells report slightly complex cause; need to parse the text with markers
            types1 = cause1.rpartition('Outgoing dependencies:')[0]
            types1_in = types1.rpartition('Incoming dependencies:')[2].rstrip('.')
            types1_out = cause1.rpartition('Outgoing dependencies:')[2]
            types2 = cause2.rpartition('Outgoing dependencies:')[0]
            types2_in = types2.rpartition('Incoming dependencies:')[2].rstrip('.')
            types2_out = cause1.rpartition('Outgoing dependencies:')[2]
            cause1_set_in = set([x.strip() for x in types1_in.split(';')])
            cause1_set_out = set([x.strip() for x in types1_out.split(';')])
            cause1_set = cause1_set_in.union(cause1_set_out)
            cause2_set_in = set([x.strip() for x in types2_in.split(';')])
            cause2_set_out = set([x.strip() for x in types2_out.split(';')])
            cause2_set = cause2_set_in.union(cause2_set_out)
            diff1 = cause1_set.difference(cause2_set)
            diff2 = cause2_set.difference(cause1_set)

            self.before_metric = len(cause2_set)
            self.after_metric = len(cause1_set)
            self.change_in_metric = len(diff1) + len(diff2)
        elif self.smell_name == D_INS_MOD or self.smell_name == D_DEE_HIE:
            # rest of the three smells differ in a metric
            m1 = re.search(r'\s*(\d+\.?\d*)', cause1)
            m2 = re.search(r'\s*(\d+\.?\d*)', cause2)
            if m1 and m2:
                no1 = float(m1.group(1))
                no2 = float(m2.group(1))
                self.before_metric = no2
                self.after_metric = no1
                self.change_in_metric = round(no1 - no2, 2)


class ArchSmell:
    def __init__(self, project_name, package_name, smell_name, cause):
        self.project_name = project_name.strip('\n')
        self.package_name = package_name
        self.smell_name = smell_name
        self.cause = cause.strip('\n')
        self.matched = False
        self.before_metric = 0
        self.after_metric = 0
        self.change_in_metric = 0

    def __str__(self):
        return self.project_name + ', ' + self.package_name + ', ' + self.smell_name + ', ' + self.cause + ', ' + str(
            self.before_metric) + ', ' + str(self.after_metric) + ', ' + str(self.change_in_metric)

    def is_smell_present(self, smell_list):
        filtered_list = filter(lambda item:
                               item.smell_name == self.smell_name and
                               item.project_name == self.project_name and
                               item.package_name == self.package_name,
                               smell_list)
        for item in filtered_list:
            if not item.matched:
                item.matched = True
                return True, item
        return False, None

    def populate_diff_metrics(self, similar_smell):
        common_str = common_substring_from_start(self.cause, similar_smell.cause)
        cause1 = self.cause.replace(common_str, '').rstrip('.')
        cause2 = similar_smell.cause.replace(common_str, '').rstrip('.')
        cause1_set = set([x.strip() for x in cause1.split(';')])
        cause2_set = set([x.strip() for x in cause2.split(';')])
        diff1 = cause1_set.difference(cause2_set)
        diff2 = cause2_set.difference(cause1_set)

        if self.smell_name == A_CYC_DEP or self.smell_name == A_UNS_DEP or self.smell_name == A_SCA_FUN or self.smell_name == A_AMB_INT:
            # this set of smells produce a list of classes and we need to figure out how many classes are different
            # prev metric, new metric, difference
            self.before_metric = len(cause2_set)
            self.after_metric = len(cause1_set)
            self.change_in_metric = len(diff1) + len(diff2)
        else:
            # rest of the three smells differ in a metric
            m1 = re.search(r'=\s*(\d+\.\d+)', cause1)
            no1 = float(m1.group(1))
            m2 = re.search(r'=\s*(\d+\.\d+)', cause2)
            no2 = float(m2.group(1))
            self.before_metric = no2
            self.after_metric = no1
            self.change_in_metric = round(no1 - no2, 2)


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
