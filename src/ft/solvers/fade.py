"""1D 时空分数阶对流-弥散方程（fADE）求解器 —— W2 待实现。

方程（无量纲形式）：

    D_t^β C = -v · ∂C/∂x + d · (-Δ)^(α/2) C ,   x ∈ (0, L), t > 0

    C(x, 0) = C0(x)
    C(0, t) = C_in(t)          （上游定浓度）
    C(L, t) = 0                （下游自由出流，先用 Dirichlet 占位）

实现要点（W2 周四完成）：
1. 时间方向：Caputo 导数用 L1 格式（ft.operators.caputo）——历史项累加；
2. 空间方向：Riesz 用谱方法（ft.operators.riesz）仅适用于周期边界；
   非周期请改移位 Grünwald-Letnikov，二者结果要在 α→2 时收敛到同一曲线；
3. 验证：β=1、α=2 时退化为经典 ADE，与解析解（误差函数）对比，
   相对误差应 < 1e-2；再做 dt 减半的自收敛阶检查（应接近 2-β）；
4. 输出：穿透曲线 C(L, t) 与不同 (α, β) 下的曲线族（图 4）。

本文件目前是**签名占位**，不要提交"能跑但没验证"的实现。
"""

import numpy as np

__all__ = ["solve_fade_1d", "breakthrough_curve"]


def solve_fade_1d(c0, c_in, dx: float, dt: float, nsteps: int,
                  v: float, d: float, alpha: float, beta: float):
    """求解 1D fADE，返回 (x, C)，C 形状为 (nsteps+1, nx)。

    参数
    ----
    c0 : array_like, shape (nx,)
        初始浓度。
    c_in : float
        上游边界浓度（常数，先用最简单的情形）。
    dx, dt : float
        空间与时间步长。
    nsteps : int
        时间步数。
    v, d : float
        流速与弥散系数。
    alpha : float
        空间分数阶阶数，1 < alpha <= 2（alpha=2 为经典二阶弥散）。
    beta : float
        时间分数阶阶数，0 < beta <= 1（beta=1 为经典一阶时间导数）。
    """
    raise NotImplementedError("W2 周四实现：先写 docs/notes/l1_scheme.md，再写求解器")


def breakthrough_curve(c, x_index: int = -1):
    """从浓度场 C(t, x) 中取某个断面的穿透曲线 C(t, x_i)。"""
    c = np.asarray(c, dtype=float)
    return c[:, x_index]
