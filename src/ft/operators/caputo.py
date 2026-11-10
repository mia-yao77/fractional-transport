"""Caputo 时间分数阶导数的 L1 格式。

定义（L1 格式，见 docs/notes/l1_scheme.md）：

    D_t^α u(t_n) ≈ 1 / (Γ(2-α) · dt^α) · Σ_{j=0}^{n-1} b_j · (u^{n-j} - u^{n-j-1})

其中 b_j = (j+1)^(1-α) - j^(1-α)，b_0 = 1。

局部截断误差 O(dt^(2-α))。α=1 时退化为经典向后差分。
"""

from math import gamma

import numpy as np

__all__ = ["l1_weights", "caputo_derivative"]


def l1_weights(alpha: float, n: int) -> np.ndarray:
    """返回 L1 格式的前 n 个权系数 b_0 … b_{n-1}。

    Parameters
    ----------
    alpha : float
        分数阶阶数，0 < alpha <= 1。
    n : int
        需要的权系数个数（= 时间步数）。

    Returns
    -------
    ndarray, shape (n,)
    """
    if not 0.0 < alpha <= 1.0:
        raise ValueError(f"alpha 必须在 (0, 1] 内，收到 {alpha}")
    if n <= 0:
        return np.empty(0)
    # b_0 = 1 单独给，避免 0**0 = 1 在 α=1 时把 b_0 算成 0
    b = np.empty(n, dtype=float)
    b[0] = 1.0
    if n > 1:
        j = np.arange(1, n, dtype=float)
        b[1:] = (j + 1.0) ** (1.0 - alpha) - j ** (1.0 - alpha)
    return b


def caputo_derivative(u, dt: float, alpha: float) -> float:
    """用 L1 格式计算时间序列 u 在**最后一个时刻**的 Caputo 导数。

    Parameters
    ----------
    u : array_like
        等间隔时间序列 u[0..N]，u[k] = u(t_k)，dt 为步长。
    dt : float
        时间步长。
    alpha : float
        分数阶阶数，0 < alpha <= 1。

    Returns
    -------
    float
        D_t^α u 在 t_N 处的近似值。
    """
    u = np.asarray(u, dtype=float).ravel()
    if u.size < 2:
        raise ValueError("u 至少需要 2 个时刻的值")
    n = u.size - 1
    b = l1_weights(alpha, n)                   # 长度 n
    increments = np.diff(u)                    # du[k] = u[k+1] - u[k]
    # Σ_{j=0}^{n-1} b_j · (u^{n-j} - u^{n-j-1}) = Σ_j b_j · du[n-1-j]
    total = float(np.dot(b, increments[::-1]))
    return total / (gamma(2.0 - alpha) * dt**alpha)
