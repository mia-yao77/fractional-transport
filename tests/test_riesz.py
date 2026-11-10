"""空间分数阶拉普拉斯的谱方法验证。

sin(kx) 是周期域上 (-Δ)^(α/2) 的特征函数，特征值 -|k|^α：
    (-Δ)^(α/2) sin(kx) = -|k|^α sin(kx)
谱方法应当**精确到机器精度**（模态不被截断时）。
"""

import numpy as np
import pytest

from ft.operators.riesz import fractional_laplacian


@pytest.mark.parametrize("alpha", [0.5, 1.0, 1.5, 2.0])
def test_eigenfunction(alpha):
    n, L = 256, 1.0
    dx = L / n
    x = np.arange(n) * dx
    k = 2.0 * np.pi / L           # 第一个非零模态
    u = np.sin(k * x)
    out = fractional_laplacian(u, dx, alpha)
    expected = -(k**alpha) * u
    assert np.max(np.abs(out - expected)) < 1e-8


def test_integer_two_is_classical_laplacian():
    n, L = 128, 1.0
    dx = L / n
    x = np.arange(n) * dx
    u = np.sin(2 * np.pi * x)
    out = fractional_laplacian(u, dx, 2.0)
    assert np.allclose(out, -(2 * np.pi) ** 2 * u, atol=1e-6)


def test_constant_input_gives_zero():
    u = np.ones(64)
    assert np.max(np.abs(fractional_laplacian(u, 0.01, 1.3))) < 1e-10
