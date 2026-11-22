#!/usr/bin/env python3
"""Write the entry image for make.fun's news-image-20261121 bounty.

The finished front page (entry.png, 1024x1024, JPEG data under a .png name)
sits next to this file. This script copies it into the folder make.fun reads,
as entry.png, and refuses to run if the file is missing or too large.
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
LIMIT = 1048576


def main() -> int:
    if not SOURCE.is_file():
        raise SystemExit(f"error: the image is missing: {SOURCE}")
    size = SOURCE.stat().st_size
    if size == 0:
        raise SystemExit(f"error: {SOURCE} is empty")
    if size > LIMIT:
        raise SystemExit(f"error: {SOURCE} is {size} bytes, over the {LIMIT}-byte limit")
    with SOURCE.open("rb") as fh:
        head = fh.read(4)
    if not (head.startswith(b"\xff\xd8\xff") or head.startswith(b"\x89PNG")):
        raise SystemExit(f"error: {SOURCE} is neither a PNG nor a JPEG file")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    written = target.stat().st_size
    if written != size or written > LIMIT:
        raise SystemExit(
            f"error: {target} is {written} bytes, expected {size} and at most {LIMIT}"
        )
    print(f"wrote {target} ({written} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
