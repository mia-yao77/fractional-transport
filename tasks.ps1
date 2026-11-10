# tasks.ps1 —— Windows 下的任务入口（等价于 Makefile）
#
# 用法（在本目录下）：
#   .\tasks.ps1 test
#   .\tasks.ps1 figures
#   .\tasks.ps1 repro
#
# 若提示"禁止运行脚本"，先执行一次：
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

param([Parameter(Position = 0)][string]$Task = "help")

$ErrorActionPreference = "Stop"
$py = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $py)) { $py = "python" }

switch ($Task) {
    "help" {
        Write-Host ".\tasks.ps1 install   安装依赖到 .venv"
        Write-Host ".\tasks.ps1 test      跑测试"
        Write-Host ".\tasks.ps1 figures   重建全部图"
        Write-Host ".\tasks.ps1 repro     清理 + 重建全部图 + 跑测试"
        Write-Host ".\tasks.ps1 dry       干跑可辨识性实验（只校验配置）"
    }
    "install" {
        & $py -m pip install -U pip
        & $py -m pip install -r requirements.txt
    }
    "test" { & $py -m pytest }
    "figures" { & $py scripts\make_figures.py }
    "repro" {
        & $py -m pytest
        & $py scripts\make_figures.py
    }
    "dry" { & $py experiments\identifiability\run.py --dry-run }
    default {
        Write-Host "未知任务：$Task"
        & $PSCommandPath help
        exit 1
    }
}
