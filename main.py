#!/usr/bin/env python3
"""Write the entry image for make.fun's news-image-20261121 bounty.

The finished front page (entry.png, 1024x1024) sits next to this file. This
script copies it into the output folder that make.fun reads, as entry.png.
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"


def main() -> int:
    if not SOURCE.is_file():
        raise SystemExit(f"error: the image is missing: {SOURCE}")
    size = SOURCE.stat().st_size
    if size > 1048576:
        raise SystemExit(
            f"error: {SOURCE} is {size} bytes, over make.fun's 1048576-byte limit"
        )
    with SOURCE.open("rb") as fh:
        head = fh.read(3)
    if head not in (b"\xff\xd8\xff", b"\x89PN"):
        raise SystemExit(f"error: {SOURCE} is not a PNG or JPEG file")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
