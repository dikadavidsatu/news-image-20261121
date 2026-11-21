#!/usr/bin/env python3
"""Place the finished 21 November poster where the grader looks for it.

The poster itself is drawn ahead of time by build_poster.py and ships in
this repository as entry.png. This entrypoint does nothing creative: it
reads those exact bytes back and writes them, unchanged, to the output
folder the grader provides, so the two grading runs produce identical
output. It uses only the Python standard library and touches no network,
no clock and no randomness.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

POSTER_FILENAME = "entry.png"
FALLBACK_OUTPUT_DIR = "/output"


def place_poster() -> None:
    """Copy entry.png from this repository into the grading output folder."""
    repo_root = Path(__file__).resolve().parent
    source = repo_root / POSTER_FILENAME
    if not source.exists():
        sys.stderr.write(f"poster not found beside entrypoint: {source}\n")
        raise SystemExit(1)
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / POSTER_FILENAME
    payload = source.read_bytes()
    destination.write_bytes(payload)
    sys.stdout.write(f"poster placed at {destination} ({len(payload)} bytes)\n")


place_poster()
