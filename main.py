"""Entry for make.fun's ai-excited-01 bounty: Make the AI judge excited.

The entry image is the entry.png beside this file. This program copies
it to the output directory as entry.png, unchanged, byte for byte.

Standard library only. No network, no randomness: two runs produce
identical output.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main() -> int:
    if not os.path.isfile(SOURCE):
        print(f"entry image not found: {SOURCE}", file=sys.stderr)
        return 1
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")
    shutil.copyfile(SOURCE, destination)
    if os.path.getsize(destination) != os.path.getsize(SOURCE):
        print("copy size mismatch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
