from postprocessor import _get_method_list, _get_type_list


def test_method_list():
    assert len(_get_method_list('./test_files')) == 748


def test_type_list():
    assert len(_get_type_list('./test_files')) == 77