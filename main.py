"""Write the entry image to the output directory.

The artwork for this entry is the PNG file bundled beside this script.
This program checks that it is a real PNG, copies it byte-for-byte to
the output directory, and verifies the copy matches the source.

Usage:
    python3 main.py

The output directory is /output by default. Set MAKEFUN_OUTPUT_DIR to
write somewhere else instead.
"""

import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SOURCE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    if not os.path.isfile(source):
        print("error: source image not found: " + source, file=sys.stderr)
        return 1

    with open(source, "rb") as handle:
        magic = handle.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        print("error: " + source + " is not a PNG file", file=sys.stderr)
        return 1

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, SOURCE_NAME)

    shutil.copyfile(source, target)

    written = os.path.getsize(target)
    expected = os.path.getsize(source)
    if written != expected:
        print(
            "error: copy size mismatch: wrote "
            + str(written)
            + " bytes, expected "
            + str(expected)
            + " bytes",
            file=sys.stderr,
        )
        return 1

    with open(target, "rb") as handle:
        copied_magic = handle.read(len(PNG_MAGIC))
    if copied_magic != PNG_MAGIC:
        print("error: copied file " + target + " is not a valid PNG",
              file=sys.stderr)
        return 1

    print("wrote " + target + " (" + str(written) + " bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
