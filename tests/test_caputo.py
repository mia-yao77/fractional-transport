"""L1 格式的解析解验证。

Caputo 导数对幂函数有精确公式：
    D_t^α t^p = Γ(p+1) / Γ(p+1-α) · t^(p-α)
取 p = 2 检验 L1 格式，相对误差应在 O(dt^(2-α)) 量级。
"""

import numpy as np
import pytest
from math import gamma

from ft.operators.caputo import caputo_derivative, l1_weights


def test_weights_basic():
    b = l1_weights(0.5, 4)
    assert b.shape == (4,)
    assert b[0] == pytest.approx(1.0)          # b_0 恒为 1
    assert np.all(np.diff(b) < 0)              # 权系数单调递减


def test_weight_alpha_one_is_backward_difference():
    # α=1 时 b_0=1，其余为 0 → 退化为向后差分
    b = l1_weights(1.0, 5)
    assert b[0] == pytest.approx(1.0)
    assert np.allclose(b[1:], 0.0, atol=1e-14)


@pytest.mark.parametrize("alpha", [0.3, 0.5, 0.7, 0.9])
def test_caputo_power_law(alpha):
    n, t_end = 4000, 1.0
    dt = t_end / n
    t = np.linspace(0.0, t_end, n + 1)
    u = t**2
    exact = gamma(3.0) / gamma(3.0 - alpha) * t_end ** (2.0 - alpha)
    approx = caputo_derivative(u, dt, alpha)
    assert abs(approx - exact) / abs(exact) < 5e-3


def test_caputo_constant_is_zero():
    u = np.full(101, 3.14)
    assert abs(caputo_derivative(u, 0.01, 0.6)) < 1e-12
