"""冒烟测试：包能导入、版本号可读、公开接口齐全。"""

import ft


def test_version():
    assert ft.__version__.count(".") == 2


def test_public_api():
    from ft import operators, solvers, stats

    assert hasattr(operators, "caputo_derivative")
    assert hasattr(operators, "fractional_laplacian")
    assert hasattr(solvers, "solve_fade_1d")
    assert hasattr(stats, "relative_l2")
