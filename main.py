#!/usr/bin/env python3
"""Check the entry image and place a verified copy in the output folder."""

import hashlib
import os
import shutil
import struct
import sys


SOURCE_NAME = "entry.png"
TARGET_DIR = "/output"
TARGET_NAME = "entry.png"
WANTED_WIDTH = 900
WANTED_HEIGHT = 600
PNG_MARK = b"\x89PNG\r\n\x1a\n"


def stop(reason):
    print(f"error: {reason}", file=sys.stderr)
    raise SystemExit(1)


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def png_size(path):
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33:
        stop("entry image is too short to hold a PNG header")
    if head[:8] != PNG_MARK:
        stop("entry image does not start with the PNG signature")
    if head[12:16] != b"IHDR":
        stop("first PNG chunk is not IHDR")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        stop(f"missing source image: {source}")

    width, height = png_size(source)
    print(f"entry image: {width}x{height}")
    if width != WANTED_WIDTH or height != WANTED_HEIGHT:
        stop(f"expected {WANTED_WIDTH}x{WANTED_HEIGHT}, got {width}x{height}")

    os.makedirs(TARGET_DIR, exist_ok=True)
    target = os.path.join(TARGET_DIR, TARGET_NAME)
    shutil.copyfile(source, target)

    before = sha256_of(source)
    after = sha256_of(target)
    print(f"source sha256: {before}")
    print(f"output sha256: {after}")
    if before != after:
        stop("output copy hash differs from source hash")
    if os.path.getsize(source) != os.path.getsize(target):
        stop("output copy size differs from source size")
    print(f"copy size verified: {os.path.getsize(target)} bytes")
    print("self-check passed: output copy matches source exactly")
    print(f"copied to {target}")


if __name__ == "__main__":
    main()
