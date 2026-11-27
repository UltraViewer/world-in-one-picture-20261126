#!/usr/bin/env python3
"""Entrypoint: draw the 26 November 2026 front page and write /output/entry.png.

Runs with no network. The drawing is fully deterministic (PIL primitives only,
fixed fonts, no randomness, no clock), so two runs write identical bytes.
"""
import os

from compose import build


def main():
    os.makedirs("/output", exist_ok=True)
    build().save("/output/entry.png", optimize=True)
    size = os.path.getsize("/output/entry.png")
    print(f"wrote /output/entry.png ({size} bytes)")


if __name__ == "__main__":
    main()
