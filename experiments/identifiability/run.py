"""可辨识性实验的入口脚本（W3 周三实现主体）。

用法（PowerShell，激活 .venv 后）：

    python experiments/identifiability/run.py --dry-run     # 今天：只校验配置
    python experiments/identifiability/run.py               # W3：真正跑扫描

--dry-run 只做三件事：读配置、打印网格规模、检查依赖是否就绪。
它**不产生任何结论**，但能证明"实验台是通的"。
"""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

CONFIG = Path(__file__).with_name("config.toml")


def load_config(path: Path = CONFIG) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def grid_size(cfg: dict) -> tuple[int, int]:
    m = cfg["model"]
    na = round((m["alpha_max"] - m["alpha_min"]) / m["alpha_step"]) + 1
    nb = round((m["beta_max"] - m["beta_min"]) / m["beta_step"]) + 1
    return na, nb


def main() -> int:
    ap = argparse.ArgumentParser(description="阶数可辨识性实验")
    ap.add_argument("--dry-run", action="store_true", help="只校验配置，不做计算")
    args = ap.parse_args()

    cfg = load_config()
    na, nb = grid_size(cfg)
    obs = cfg["observation"]

    print("=" * 56)
    print("配置：", CONFIG.name)
    print(f"α 网格点 {na} × β 网格点 {nb} = {na * nb} 组正演")
    print(f"观测断面 {obs['sections']} 个；噪声 {obs['noise_levels']}")
    print(f"判据阈值 {obs['threshold']:.0%}（相对 L2 距离）")
    print(f"数值：nx={cfg['numerics']['nx']}，t_end={cfg['numerics']['t_end']:.0f}s")
    print("=" * 56)

    if args.dry_run:
        print("dry-run 通过：配置文件可读、网格可算、路径正常。")
        print("下一步（W3 周三）：实现 ft.stats.identifiability.summarize_region，"
              "再跑真实扫描。")
        return 0

    from ft.stats.identifiability import summarize_region  # noqa: F401
    from ft.solvers.fade import solve_fade_1d  # noqa: F401

    print("尚未实现：请先完成 W2 的 solve_fade_1d 与 W3 的 summarize_region。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
