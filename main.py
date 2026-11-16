"""The phoenix who refused to stay painted.

A blazing watercolor phoenix smashes out of its own painting through
the picture frame into a sunlit artist's studio, wings spanning edge
to edge, embers turning into butterflies as they rise. The laughing
artist reaches out with her brush still mid-stroke while a startled
ginger cat leaps back from the easel. Pinned to the easel, a small
note reads: "It refused to stay painted."

Attempt 5: a fresh rebuild of the phoenix breakout in a single
recorded session, aiming past attempt 3's 96.16%. The entry image is
900x600; main.py also reads those dimensions straight from the PNG
header and prints them, so a wrong-sized image is caught at a glance.

Copies the entry image to /output/entry.png.
Standard library only.
"""

import hashlib
import shutil
import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_dimensions(data):
    """Read width and height from the PNG IHDR chunk."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    source_bytes = source.read_bytes()
    if not source_bytes.startswith(PNG_MAGIC):
        print("error: entry.png is not a valid PNG", file=sys.stderr)
        raise SystemExit(1)
    width, height = png_dimensions(source_bytes)
    print(f"dimensions: {width}x{height}")
    if (width, height) != (900, 600):
        print("error: entry.png must be 900x600", file=sys.stderr)
        raise SystemExit(1)
    output_dir = Path("/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"
    shutil.copyfile(source, destination)
    # Determinism self-check: the output must be byte-identical to the source.
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    output_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
    print(f"source: {source}")
    print(f"output: {destination}")
    print(f"sha256: {output_hash}")
    print(f"match: {source_hash == output_hash}")
    if source_hash != output_hash:
        print("error: determinism self-check failed", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
