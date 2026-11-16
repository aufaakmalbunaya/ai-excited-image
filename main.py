"""Copy entry.png to the output directory.

The image beside this script is the entry artwork. This program checks
that it is a real PNG, copies it byte-for-byte into the directory named
by MAKEFUN_OUTPUT_DIR (or /output by default), and confirms the copy
matches the source in size.
"""

import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SOURCE_NAME = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    with open(source, "rb") as handle:
        magic = handle.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        print(f"error: {source} is not a PNG file", file=sys.stderr)
        return 1

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, SOURCE_NAME)

    shutil.copyfile(source, target)

    written = os.path.getsize(target)
    expected = os.path.getsize(source)
    if written != expected:
        print(
            f"error: copy size mismatch: wrote {written} bytes, "
            f"expected {expected} bytes",
            file=sys.stderr,
        )
        return 1

    with open(target, "rb") as handle:
        copied_magic = handle.read(len(PNG_MAGIC))
    if copied_magic != PNG_MAGIC:
        print(f"error: copied file {target} is not a valid PNG", file=sys.stderr)
        return 1

    print(f"wrote {target} ({written} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
