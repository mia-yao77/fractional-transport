# fractional-transport

分数阶反常运移模型的**快速正演**与**统计反演**。可辨识性实验的全部代码与图都在这里。

- 科学问题：在什么观测条件下，分数阶模型的阶数 α、β 能被数据唯一确定？
- 方法：L1 格式（时间分数阶）+ 谱方法（空间分数阶）+ 相对 L2 距离 / profile likelihood / 贝叶斯 MCMC
- 场景：地下水溶质运移；后续落到饱和-非饱和 Richards

## 安装（Windows / PowerShell）

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # 命令行前出现 (.venv) 才算激活
python -m pip install -U pip
pip install -r requirements.txt
```

PowerShell 提示"禁止运行脚本"时，先执行一次：
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Linux / macOS 用 `source .venv/bin/activate`。

## 跑起来

| 做什么 | Windows | Linux / CI |
|---|---|---|
| 跑测试 | `.\tasks.ps1 test` | `make test` |
| 重建全部图 | `.\tasks.ps1 figures` | `make figures` |
| 清理 + 重建 + 测试 | `.\tasks.ps1 repro` | `make repro` |
| 干跑可辨识性实验 | `.\tasks.ps1 dry` | `python experiments/identifiability/run.py --dry-run` |

## 目录

```
src/ft/operators/   caputo.py（L1 格式）· riesz.py（谱方法分数阶拉普拉斯）
src/ft/solvers/     fade.py（1D 时空分数阶对流-弥散，W2 实现）
src/ft/stats/       metrics.py（相对 L2 距离）· identifiability.py（W3 实现）
experiments/        可辨识性实验：config.toml + run.py
tests/              解析解对照 + 特征函数验证 + 冒烟测试
docs/               glossary（术语）· roadmap（方向陈述）· weekly（周报）· notes（文献笔记）
scripts/            make_figures.py（所有图由它生成）
```

## 当前状态

| 模块 | 状态 | 验收 |
|---|---|---|
| Caputo L1 格式 | ✅ 已实现 | 对 t² 的解析解相对误差 < 5e-3（4 个 α 值） |
| Riesz 谱方法 | ✅ 已实现 | sin(kx) 特征函数精确到 1e-8 |
| 相对 L2 距离 | ✅ 已实现 | 冒烟测试 |
| fADE 求解器 | ⬜ W2 | β=1、α=2 退化到经典 ADE，误差 < 1e-2 |
| 可辨识性扫描 | ⬜ W3 | 图 5 可接受区域 + 图 6 观测设计 |

## 复现约定

1. 每条图都能由 `scripts/make_figures.py` 生成，图上角标写 commit hash；
2. 随机数 seed 统一放在 `experiments/*/config.toml`，禁止裸 `np.random`；
3. 测试里断言"数值 vs 解析"的相对误差阈值，CI 变红就是代码错；
4. 里程碑打 tag：`v0.1-w1` / `v0.2-w2` / `v0.3-w3`。

## 引用

见 `CITATION.cff`。代码 MIT，论文另议。
