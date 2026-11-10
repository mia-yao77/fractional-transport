"""重建全部图 —— 每条图都必须能由这一个脚本生成。

约定（可复现五条规则之二）：
1. 每张图保存时把 git commit hash 写进图角标；
2. 随机过程一律从 config 里读 seed；
3. 图输出到 docs/figures/，文件名固定（fig1_… / fig2_…）。

目前只有占位实现：W1 结束时补 fig1，W2 结束时补 fig2/fig4，W3 补 fig5/fig6。
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "figures"


def commit_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True,
            stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "no-git"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"输出目录: {OUT}")
    print(f"commit  : {commit_hash()}")
    print("尚未实现具体图。W1 先补 fig1_landscape；W2 补 fig2_verify、fig4_breakthrough。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
