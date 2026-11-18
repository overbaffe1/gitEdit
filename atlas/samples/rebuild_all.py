#!/usr/bin/env python3
"""Пересобрать все 111 SVG склада одной командой. Запуск из корня."""
import subprocess, pathlib, sys
root=pathlib.Path(__file__).resolve().parents[2]
samples=sorted((root/"atlas/samples").glob("*.py"))
# filter to our warehouse generators (those that write to assets/*.svg)
ok=0
for py in samples:
    try:
        subprocess.run([sys.executable, str(py)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        print(f"  {py.name} OK")
        ok+=1
    except Exception as e:
        print(f"  {py.name} SKIP: {e}")
print(f"Rebuilt {ok}/{len(samples)} generators")
