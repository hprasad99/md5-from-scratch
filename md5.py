"""
Pure Python MD5 implementation (RFC1321).
Usage:
    python md5.py "hello"
    python md5.py --file path/to/file
    echo -n "hello" | python md5.py
"""

import struct
import math
import sys

# Per-round shift amounts
S = [
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21,
]

# Precomputed table: K[i] = floor(2^32 * |sin(i+1)|)
K = [int(2**32 * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]

# Initial hash values
INIT = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)


def left_rotate(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def pad(message: bytes) -> bytes:
    """Pad message to a mulitple of 512 bits (64bytes)"""
    length_bits = (len(message) * 8) & 0xFFFFFFFFFFFFFFFF
    message += b"\x80"
    message += b"\x00" * (-(len(message) + 8) % 64)
    message += struct.pack("<Q", length_bits)
    return message


def process_chunk(chunk: bytes, state: tuple) -> tuple:
    """Process a single 512-bit (64-byte) chunk."""
    assert len(chunk) == 64
    M = struct.unpack("<16I", chunk)  # 16 * 32-bit words, little-endian
    a, b, c, d = state

    for i in range(64):
        if i < 16:
            f = (b & c) | (~b & d)
            g = i
        elif i < 32:
            f = (b & d) | (c & ~d)
            g = (5 * i + 1) % 16
        elif i < 48:
            f = b ^ c ^ d
            g = (3 * i + 5) % 16
        else:
            f = c ^ (b | ~d)
            g = (7 * i) % 16

        f = (f + a + K[i] + M[g]) & 0xFFFFFFFF
        a = d
        d = c
        c = b
        b = (b + left_rotate(f, S[i])) & 0xFFFFFFFF

    return (
        (state[0] + a) & 0xFFFFFFFF,
        (state[1] + b) & 0xFFFFFFFF,
        (state[2] + c) & 0xFFFFFFFF,
        (state[3] + d) & 0xFFFFFFFF,
    )


def md5(data: bytes) -> str:
    """Return the MD5 hex digest of data."""
    padded = pad(data)
    state = INIT
    for i in range(0, len(padded), 64):
        state = process_chunk(padded[i : i + 64], state)
    return struct.pack("<4I", *state).hex()


# ---------------------------------------------------
# CLI
# ---------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Pure-Python MD5")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("text", nargs="?", help="String to hash")
    group.add_argument("--file", "-f", help="File to hash")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "rb") as fh:
            data = fh.read()
        print(f"{md5(data)} {args.file}")
    elif args.text is not None:
        print(md5(args.text.encode()))
    elif not sys.stdin.isatty():
        data = sys.stdin.buffer.read()
        print(md5(data))
    else:
        parser.print_help()
