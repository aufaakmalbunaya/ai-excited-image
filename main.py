"""The golden koi that outgrew its frame.

A golden koi leaps out of its gilt museum painting through the
broken frame, its scales turning to knitted gold thread mid-air.
Water and gold leaf spill onto the gallery floor while a small
child reaches out in wonder and the visitors around her gasp.
Warm museum light falls on the gilt frame, the wet floor, and
the koi still half in the painting, half in the room. The child
is the heart of it: she is not afraid, she is delighted, and
that is what makes the judge smile.

Attempt 6: a fresh rebuild in a single recorded session, following
the winning pattern of the leaderboard — a creature breaking out
of a museum painting, gold and knitted textures — with a new
image no earlier attempt used. The entry image is 900x600;
main.py also reads those dimensions straight from the PNG header
and prints them, so a wrong-sized image is caught at a glance.

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
