"""周期域上一维 Riesz 分数阶拉普拉斯算子的谱方法实现。

约定（与 W2 的正演一致）：

    (-Δ)^(α/2) u  ←→  |k|^α · û(k)          （傅里叶乘子）
    α = 1  →  -Δ 的"半阶"，α = 2 → 经典 -Δ

空间分数阶对流弥散方程（fADE）中的弥散项就是 -D · (-Δ)^(α/2)。
只在**周期边界**下严格成立；非周期问题请改用移位 Grünwald-Letnikov
（Meerschaert & Tadjeran 2004），不要直接套用本模块。
"""

import numpy as np

__all__ = ["wavenumbers", "fractional_laplacian"]


def wavenumbers(n: int, dx: float) -> np.ndarray:
    """FFT 对应的波数（rad / 单位长度），按 numpy.fft 的顺序排列。"""
    return 2.0 * np.pi * np.fft.fftfreq(n, d=dx)


def fractional_laplacian(u, dx: float, alpha: float) -> np.ndarray:
    """计算 (-Δ)^(α/2) u，周期边界，谱方法。

    Parameters
    ----------
    u : array_like, shape (n,)
        网格上的函数值，网格点 x_j = j * dx。
    dx : float
        空间步长。
    alpha : float
        分数阶阶数，0 < alpha <= 2。

    Returns
    -------
    ndarray, shape (n,)
        实部（输入为实值时结果也是实值）。
    """
    if not 0.0 < alpha <= 2.0:
        raise ValueError(f"alpha 必须在 (0, 2] 内，收到 {alpha}")
    u = np.asarray(u, dtype=float).ravel()
    k = wavenumbers(u.size, dx)
    return np.real(np.fft.ifft(-np.abs(k) ** alpha * np.fft.fft(u)))
