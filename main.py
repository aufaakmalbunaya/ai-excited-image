"""Watercolor phoenix breaks out of the canvas.

A phoenix bursts off a painted canvas in a sunlit artist's studio,
embers turning into butterflies, while the artist laughs and a ginger
cat leaps back in surprise. Attempt 4: a breakout moment, following
the pattern of a creature leaving its artwork for the real world.

Copies the entry image to /output/entry.png.
Standard library only.
"""

import hashlib
import shutil
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    source_bytes = source.read_bytes()
    if not source_bytes.startswith(PNG_MAGIC):
        print("error: entry.png is not a valid PNG", file=sys.stderr)
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
