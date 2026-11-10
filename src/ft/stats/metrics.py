"""两条曲线之间的距离度量 —— 可辨识性实验的基本工具。

判据（写死，事后不得修改）：
    相对 L2 距离 < 2%  →  在噪声水平下判为"实践上不可辨识"
"""

import numpy as np

__all__ = ["relative_l2", "normalized_curve", "distance_matrix"]


def relative_l2(a, b) -> float:
    """相对 L2 距离 ‖a - b‖₂ / ‖a‖₂。

    a 是参考曲线，b 是待比较曲线。两者长度必须一致。
    """
    a = np.asarray(a, dtype=float).ravel()
    b = np.asarray(b, dtype=float).ravel()
    if a.size != b.size:
        raise ValueError(f"长度不一致：{a.size} vs {b.size}")
    denom = np.linalg.norm(a)
    if denom == 0.0:
        raise ValueError("参考曲线全零，相对距离无定义")
    return float(np.linalg.norm(a - b) / denom)


def normalized_curve(c, t=None):
    """把穿透曲线归一化到 [0, 1]，便于跨阶数比较。

    若给定时间轴，用梯形积分做面积归一；否则按最大值归一。
    """
    c = np.asarray(c, dtype=float).ravel()
    if t is None:
        peak = c.max()
        return c / peak if peak > 0 else c
    area = float(np.trapezoid(c, np.asarray(t, dtype=float)))
    return c / area if area > 0 else c


def distance_matrix(curves, reference) -> np.ndarray:
    """每条曲线与参考曲线的相对 L2 距离。

    Parameters
    ----------
    curves : sequence of array_like
        待比较的曲线集合（每个元素是一条曲线）。
    reference : array_like
        参考曲线。

    Returns
    -------
    ndarray, shape (len(curves),)
    """
    return np.array([relative_l2(reference, c) for c in curves], dtype=float)
