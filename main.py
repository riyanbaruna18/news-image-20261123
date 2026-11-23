#!/usr/bin/env python3
"""news-image-20261123 entry point.

Deterministically writes the competition entry image to /output/entry.png.

No network access, no randomness, no timestamps: the image bytes are
stored in this repo as entry.png and are copied verbatim to the output
path, so two runs always produce byte-identical output.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT = Path(os.environ.get("OUTPUT_PATH", "/output/entry.png"))


def main() -> int:
    if not SOURCE.is_file():
        print(f"missing source image: {SOURCE}", file=sys.stderr)
        return 1
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
