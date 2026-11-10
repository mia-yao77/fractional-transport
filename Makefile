# 注意：Windows 默认没有 make。本地请用 tasks.ps1，CI（Ubuntu）用本文件。
PY ?= python

.PHONY: help env install test figures repro clean

help:
	@echo "make install  安装依赖"
	@echo "make test     跑测试"
	@echo "make figures  重建全部图"
	@echo "make repro    从零重建全部图（CI 用它）"
	@echo "make clean    清理缓存"

install:
	$(PY) -m pip install -U pip
	$(PY) -m pip install -r requirements.txt

test:
	$(PY) -m pytest

figures:
	$(PY) scripts/make_figures.py

repro: clean figures test

clean:
	$(PY) -c "import shutil,pathlib;[shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"
