# This script reads the output generated by DesigniteJava tool
# and emits the output indexed by filepath i.e.,
# Filepath, smell, project, package, type, method, cause, start_line_no

import os.path
import sys
from .model import Type, Method, ImplSmell, DesignSmell, ArchSmell

def _get_type_list(out_path):
    type_file = os.path.join(out_path, 'TypeMetrics.csv')
    type_list = list()
    if os.path.exists(type_file):
        is_first_line = True
        with open(type_file, 'r', encoding='utf8', errors='ignore') as file:
            for line in file:
                if is_first_line:
                    is_first_line = False
                    continue
                tokens = line.split(',')
                if len(tokens) > 15:
                    type_list.append(Type(tokens[0], tokens[1],
                                          tokens[2], tokens[14], tokens[15]))
    return type_list


def _get_method_list(out_path):
    method_file = os.path.join(out_path, 'MethodMetrics.csv')
    method_list = list()
    if os.path.exists(method_file):
        is_first_line = True
        with open(method_file, 'r', encoding='utf8', errors='ignore') as file:
            for line in file:
                if is_first_line:
                    is_first_line = False
                    continue
                tokens = line.split(',')
                if len(tokens) > 7:
                    method_list.append(Method(tokens[0], tokens[1],
                                              tokens[2], tokens[3], tokens[7]))
    return method_list


def _get_impl_smells_list(out_path):
    impl_file = os.path.join(out_path, 'ImplementationSmells.csv')
    smell_list = list()
    if os.path.exists(impl_file):
        is_first_line = True
        with open(impl_file, 'r', encoding='utf8', errors='ignore') as file:
            for line in file:
                if is_first_line:
                    is_first_line = False
                    continue
                tokens = line.split(',')
                if len(tokens) > 6:
                    smell_list.append(ImplSmell(tokens[0], tokens[1],
                                                tokens[2], tokens[3], tokens[4], tokens[5], tokens[6]))
    return smell_list


def _process_impl_smells(type_list, method_list, impl_smell_list, out_path):
    out_file = os.path.join(out_path, 'postprocessed.csv')
    with open(out_file, 'w', encoding='utf8', errors='ignore') as file:
        file.write('Filepath,smell,project,package,type,method,cause,start_line_no\n')
        for smell in impl_smell_list:
            methods = [item for item in method_list if
                       smell.project_name == item.project_name and
                       smell.package_name == item.package_name and
                       smell.type_name == item.type_name and
                       smell.method_name == item.method_name and
                       smell.m_start_line_no == item.start_line_no]
            if len(methods) > 1:
                print('overridden methods detected')
            if len(methods) == 0:
                print('method not found')
                continue
            target_method = methods[0]
            types = [item for item in type_list if
                     smell.project_name == item.project_name and
                     smell.package_name == item.package_name and
                     smell.type_name == item.type_name]
            if len(types) > 1:
                print('more than one classes found')
            if len(types) == 0:
                print('type not found')
                continue
            target_type = types[0]
            line = target_type.file_path + ',' + smell.smell_name + ',' +\
                    target_type.project_name + ',' + target_type.package_name + ',' +\
                    target_type.type_name + ',' + target_method.method_name + ',' +\
                    smell.cause + ',' + target_method.start_line_no
            file.write(line)


def _get_design_smells_list(out_path):
    design_file = os.path.join(out_path, 'DesignSmells.csv')
    smell_list = list()
    if os.path.exists(design_file):
        is_first_line = True
        with open(design_file, 'r', encoding='utf8', errors='ignore') as file:
            for line in file:
                if is_first_line:
                    is_first_line = False
                    continue
                tokens = line.split(',')
                if len(tokens) > 4:
                    smell_list.append(DesignSmell(tokens[0], tokens[1],
                                                tokens[2], tokens[3], tokens[4]))
    return smell_list


def _process_design_smells(type_list, design_smell_list, out_path):
    out_file = os.path.join(out_path, 'postprocessed.csv')
    with open(out_file, 'a', encoding='utf8', errors='ignore') as file:
        for smell in design_smell_list:
            types = [item for item in type_list if
                     smell.project_name == item.project_name and
                     smell.package_name == item.package_name and
                     smell.type_name == item.type_name]
            if len(types) > 1:
                print('more than one classes found')
            if len(types) == 0:
                print('type not found')
                continue
            target_type = types[0]
            line = target_type.file_path + ',' + smell.smell_name + ',' + \
                   target_type.project_name + ',' + target_type.package_name + ',' + \
                   target_type.type_name + ',,' + \
                   smell.cause + ',' + target_type.start_line_no
            file.write(line)


def _get_arch_smells_list(out_path):
    arch_file = os.path.join(out_path, 'ArchitectureSmells.csv')
    smell_list = list()
    if os.path.exists(arch_file):
        is_first_line = True
        with open(arch_file, 'r', encoding='utf8', errors='ignore') as file:
            for line in file:
                if is_first_line:
                    is_first_line = False
                    continue
                tokens = line.split(',')
                if len(tokens) > 3:
                    smell_list.append(ArchSmell(tokens[0], tokens[1],
                                                  tokens[2], tokens[3]))
    return smell_list


def _process_arch_smells(type_list, arch_smell_list, out_path):
    out_file = os.path.join(out_path, 'postprocessed.csv')
    with open(out_file, 'a', encoding='utf8', errors='ignore') as file:
        for smell in arch_smell_list:
            types = [item for item in type_list if
                     smell.project_name == item.project_name and
                     smell.package_name == item.package_name]
            if len(types) == 0:
                # check if it 'dense structure' smell. In this case, all packages are marked as smelly.
                if smell.package_name == '<All packages>':
                    types = [item for item in type_list if
                             smell.project_name == item.project_name]
                    if len(types) == 0:
                        print('no matching types found')
                        continue

            for type in types:
                line = type.file_path + ',' + smell.smell_name + ',' + \
                       type.project_name + ',' + type.package_name + ',' + \
                       type.type_name + ',,' + \
                       smell.cause + ',' + type.start_line_no
                file.write(line)


def process(out_path):
    type_list = _get_type_list(out_path)
    method_list = _get_method_list(out_path)
    impl_smell_list = _get_impl_smells_list(out_path)
    _process_impl_smells(type_list, method_list, impl_smell_list, out_path)
    design_smell_list = _get_design_smells_list(out_path)
    _process_design_smells(type_list, design_smell_list, out_path)
    arch_smell_list = _get_arch_smells_list(out_path)
    _process_arch_smells(type_list, arch_smell_list, out_path)


def _get_impl_smells_list_dpy(out_path):
    smell_list = list()
    for filename in os.listdir(out_path):
        if filename.endswith('implementation_smells.csv'):
            impl_file = os.path.join(out_path, filename)
            if os.path.exists(impl_file):
                print('processing ' + impl_file)
                is_first_line = True
                with open(impl_file, 'r', encoding='utf8', errors='ignore') as file:
                    for line in file:
                        if is_first_line:
                            is_first_line = False
                            continue
                        tokens = line.split(',')
                        if len(tokens) > 7:
                            # Package	Module	Class	Smell	Function/Method	Line no	File	Details
                            # def __init__(self, project_name, package_name, type_name, method_name, smell_name, cause, line_no):
                            smell_list.append(ImplSmell('dpy', tokens[0], tokens[1] + '.' +
                                                        tokens[2], tokens[4], tokens[3], tokens[7], tokens[5]))
    return smell_list


def _get_design_smells_list_dpy(out_path):
    smell_list = list()
    for filename in os.listdir(out_path):
        if filename.endswith('design_smells.csv'):
            design_file = os.path.join(out_path, filename)
            if os.path.exists(design_file):
                is_first_line = True
                with open(design_file, 'r', encoding='utf8', errors='ignore') as file:
                    for line in file:
                        if is_first_line:
                            is_first_line = False
                            continue
                        tokens = line.split(',')
                        if len(tokens) > 6:
                            smell_list.append(DesignSmell('prj', tokens[0], tokens[3],
                                                          tokens[2], tokens[6]))
    return smell_list




if __name__ == '__main__':
    if len(sys.argv) > 1:
        process(sys.argv[1])
    else:
        print('Arg error: specify designite output folder path as the parameter.')
