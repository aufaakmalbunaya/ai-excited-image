"""Attempt 8: copy the recorded-session image to /output/entry.png.

Standard library only. Deterministic: the output bytes are exactly the
input bytes, so repeated runs produce identical files.
"""

import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    with open(SOURCE, "rb") as f:
        source_digest = hashlib.sha256(f.read()).hexdigest()
    with open(DEST, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    if digest != source_digest:
        print("output does not match source", file=sys.stderr)
        return 1
    print("wrote {} ({} bytes, sha256 {})".format(
        DEST, os.path.getsize(DEST), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
