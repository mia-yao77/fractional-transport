"""阶数的可辨识性分析 —— W3 待实现。

实验设计（见 docs/exp_identifiability.md 与计划书附录 C）：

1. 在 α ∈ [0.3, 1.0] × β ∈ [0.3, 1.0] 的 15×15 网格上正演穿透曲线；
2. 对每组参数计算它与参考曲线的相对 L2 距离（ft.stats.metrics.relative_l2）；
3. 以「相对差异 < 2%」为阈值，画出 α–β 平面上的**可接受区域**；
4. 改变观测断面数（1/3/5）与噪声水平（1%/5%/10%），看区域如何变化。

输出：fig5_acceptance.png（可接受区域等高线）、fig6_design.png（多面板）。

判据必须事先写死，不允许"看图后调阈值"——那是自欺。
"""

import numpy as np

__all__ = ["acceptance_mask", "summarize_region"]


def acceptance_mask(distances, threshold: float = 0.02) -> np.ndarray:
    """把距离数组转成布尔掩码：True 表示落在可接受区域内。"""
    d = np.asarray(distances, dtype=float)
    return d < threshold


def summarize_region(mask, alpha_grid, beta_grid):
    """统计可接受区域的基本形状，供画图与结论使用。

    返回 dict：
        count      —— 区域内参数组合个数
        alpha_span —— α 方向跨度
        beta_span  —— β 方向跨度
        diagonal   —— 是否呈"斜脊"（强 trade-off 的特征）
                     （用区域内 (α, β) 的相关系数判断，|ρ| > 0.5 记为 True）
    """
    raise NotImplementedError("W3 周三实现：网格扫描 + 距离矩阵 + 区域统计")
