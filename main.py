#!/usr/bin/env python3
"""news-image-20261123 entry point.

Deterministically writes the competition entry image to /output/entry.png.

No network access, no randomness, no timestamps: the image bytes are
stored in this repo as entry.png and are copied verbatim to the output
path, so two runs always produce byte-identical output.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT = Path(os.environ.get("OUTPUT_PATH", "/output/entry.png"))

MAX_BYTES = 1 << 20          # competition cap: image at most 1 MiB
MAX_SIDE = 1024              # competition cap: at most 1024x1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def check_png(path: Path) -> tuple[int, int, int]:
    """Return (width, height, size) of a PNG, failing loudly otherwise."""
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"{path}: {len(data)} bytes exceeds {MAX_BYTES}")
    if data[:8] != PNG_SIGNATURE:
        raise ValueError(f"{path}: not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"{path}: {width}x{height} exceeds {MAX_SIDE}x{MAX_SIDE}")
    return width, height, len(data)


def main() -> int:
    if not SOURCE.is_file():
        print(f"missing source image: {SOURCE}", file=sys.stderr)
        return 1
    try:
        width, height, size = check_png(SOURCE)
    except ValueError as exc:
        print(f"invalid source image: {exc}", file=sys.stderr)
        return 1
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(f"wrote {OUTPUT} ({size} bytes, {width}x{height}, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
