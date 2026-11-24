#!/usr/bin/env python3
"""Entry for make.fun bounty 'Sum up 24 November's world news in one image'
(news-image-20261124).

Writes the prepared front-page image to /output/entry.png.
The image is held in this repository as asset.png; this program copies its
bytes exactly, uses no network, and produces identical bytes on every run.
An ENTRY_OUTPUT environment variable may override the destination for
local testing only.
"""
import os
import shutil
import stat
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    asset = here / "asset.png"
    if not asset.is_file():
        print(f"missing asset: {asset}", file=sys.stderr)
        return 1

    dest = Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.png"))
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        dest = Path.cwd() / "output" / "entry.png"
        dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        os.umask(0o022)
    except OSError:
        pass
    shutil.copyfile(asset, dest)
    try:
        os.chmod(dest, 0o644)
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
