#!/usr/bin/env python3
"""Publish the finished front page for the 24 November news-image bounty.

The artwork itself ships inside this repository as ``asset.png``: a
single-page newspaper front page that sums up Tuesday 24 November 2026.
This program is only the delivery step. It checks that the stored page
really is a PNG, then places it at ``/output/entry.png`` exactly as
stored, so the judged image is the page the repository holds, byte for
byte, on every run. Nothing here touches the network and nothing is
random: same repository in, same image out.
"""

import os
import sys
from pathlib import Path

PAGE_FILE = "asset.png"
DESTINATION = Path("/output/entry.png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_page() -> bytes:
    """Load the stored front page, refusing anything that is not a PNG."""
    page_path = Path(__file__).resolve().parent / PAGE_FILE
    if not page_path.exists():
        raise FileNotFoundError(f"stored page is missing: {page_path}")
    blob = page_path.read_bytes()
    if not blob.startswith(PNG_SIGNATURE):
        raise ValueError(f"{page_path} does not start with a PNG signature")
    return blob


def publish(blob: bytes, target: Path) -> Path:
    """Write via a neighbouring temp file so the result is never partial."""
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = target.with_name(target.name + ".part")
    staging.write_bytes(blob)
    os.replace(staging, target)
    return target


def run() -> int:
    try:
        blob = read_page()
        written = publish(blob, DESTINATION)
    except (OSError, ValueError) as problem:
        print(f"could not publish the front page: {problem}", file=sys.stderr)
        return 1
    print(f"front page published: {written} ({len(blob)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
