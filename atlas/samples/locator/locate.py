#!/usr/bin/env python3
"""Locate an oriented 6x6 binary patch in a published toroidal pattern; no origin given."""
import argparse
import json
from pathlib import Path
from codebook import load,book,parse_patch,locate

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('pattern',type=Path);p.add_argument('patch',type=Path);args=p.parse_args()
    try:result=locate(book(load(args.pattern)),parse_patch(args.patch.read_text()))
    except ValueError as e:p.error(str(e))
    print(json.dumps(result,indent=2))
    if not result['accepted']:raise SystemExit(2)
