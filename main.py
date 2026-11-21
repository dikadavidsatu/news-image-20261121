#!/usr/bin/env python3
"""Entrypoint for the news-image-20261121 make.fun entry.

The poster is rendered ahead of time by build_poster.py and shipped in
this repository as ``entry.png``. This program only places that exact
file at ``$MAKEFUN_OUTPUT_DIR/entry.png`` (``/output`` when the variable
is not set), so both grading runs produce identical bytes.

Standard library only, no network, no clock, no randomness. The copy
is byte-for-byte, so the two grading runs write identical output.
"""

import os
import shutil
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    poster = here / "entry.png"
    if not poster.is_file():
        print(f"entry.png missing from {here}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(poster, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
