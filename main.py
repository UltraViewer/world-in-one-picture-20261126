#!/usr/bin/env python3
"""Emit the pre-rendered front page for the 26 November news image.

The artwork is produced ahead of time by compose.py and shipped next to
this file as entry.png. This program only checks that file and copies it
into the grader's output directory, so it needs nothing beyond the
standard library: no image code, no fonts, no sibling modules.
"""
import os
import shutil
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(source):
        return fail("entry.png is missing next to main.py (%s)" % source)

    with open(source, "rb") as handle:
        blob = handle.read()

    if len(blob) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit"
                    % len(blob))
    if blob[:8] != PNG_MAGIC:
        return fail("entry.png does not start with the PNG signature")
    if len(blob) < 33 or blob[12:16] != b"IHDR":
        return fail("entry.png has no IHDR chunk where one is expected")
    width, height = struct.unpack(">II", blob[16:24])
    if (width, height) != (1024, 1024):
        return fail("entry.png is %dx%d, expected 1024x1024"
                    % (width, height))

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, target)
    print("wrote %s (%d bytes)" % (target, len(blob)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
