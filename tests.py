from postprocessor import _get_method_list, _get_type_list, _get_impl_smells_list, _get_design_smells_list, \
    _get_arch_smells_list


def test_method_list():
    assert len(_get_method_list('./test_files')) == 748


def test_type_list():
    assert len(_get_type_list('./test_files')) == 77


def test_get_impl_smells_list():
    assert len(_get_impl_smells_list('./test_files')) == 226


def test_get_design_smells_list():
    assert len(_get_design_smells_list('./test_files')) == 56


def test_get_arch_smells_list():
    assert len(_get_arch_smells_list('./test_files')) == 43
