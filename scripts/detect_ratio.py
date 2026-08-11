#!/usr/bin/env python3
"""Detect an image's aspect ratio and report which target ratios still need to be generated.

Usage:
    python3 detect_ratio.py <image> [ratios...]

    ratios: target ratios like 4:3 3:4 16:9 2.35:1 (default: 4:3 3:4 16:9)

Output: one line per target ratio — GENERATE or SKIP — plus the source dimensions.
Supports PNG / JPEG / GIF with stdlib only. For other formats, fall back to:
    sips -g pixelWidth -g pixelHeight <image>
"""
import struct
import sys

TOLERANCE = 0.01  # 1% relative tolerance on the aspect ratio


def png_size(f):
    f.seek(8)
    length, chunk = struct.unpack(">I4s", f.read(8))
    if chunk != b"IHDR":
        return None
    w, h = struct.unpack(">II", f.read(8))
    return w, h


def gif_size(f):
    f.seek(6)
    w, h = struct.unpack("<HH", f.read(4))
    return w, h


def jpeg_size(f):
    f.seek(2)
    while True:
        byte = f.read(1)
        while byte and byte != b"\xff":
            byte = f.read(1)
        marker = f.read(1)
        if not marker:
            return None
        m = marker[0]
        if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
            continue
        length = struct.unpack(">H", f.read(2))[0]
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            data = f.read(5)
            h, w = struct.unpack(">HH", data[1:5])
            return w, h
        f.seek(length - 2, 1)


def image_size(path):
    with open(path, "rb") as f:
        magic = f.read(12)
        if magic[:8] == b"\x89PNG\r\n\x1a\n":
            return png_size(f)
        if magic[:6] in (b"GIF87a", b"GIF89a"):
            return gif_size(f)
        if magic[:2] == b"\xff\xd8":
            return jpeg_size(f)
    return None


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    targets = sys.argv[2:] or ["4:3", "3:4", "16:9"]

    size = image_size(path)
    if not size:
        sys.exit(f"ERROR: unsupported format for {path}; use `sips -g pixelWidth -g pixelHeight` instead")
    w, h = size
    src = w / h
    print(f"source: {w}x{h} ({src:.4f})")

    for t in targets:
        tw, th = (float(x) for x in t.split(":"))
        target = tw / th
        status = "SKIP" if abs(src / target - 1) <= TOLERANCE else "GENERATE"
        print(f"{t}: {status}")


if __name__ == "__main__":
    main()
