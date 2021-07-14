import os.path
import sys
from model import Type,Method


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
                if len(tokens) > 14:
                    type_list.append(Type(tokens[0], tokens[1],
                                          tokens[2], tokens[13], tokens[14]))
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


def process(out_path):
    type_list = _get_type_list(out_path)
    print(len(type_list))
    method_list = _get_method_list(out_path)
    print(len(method_list))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        process(sys.argv[1])
    else:
        print('Arg error: specify designite output folder path as the parameter.')
