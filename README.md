# MD5 From Scratch

A pure python implementation of the MD5 hashing algorithm, built from scratch with zero external dependencies. Written for learning - every line is commented and follows [RFC 1321](https://www.ietf.org/rfc/rfc1321.txt) exactly.

## What is MD5?

MD5 (Message Digest 5) is a cryptographic hash function designed by Ron Rivest in 1992. It takes any input and producs a fixed 128-bit (32 hex character) digest.

```
"hello"  →  5d41402abc4b2a76b9719d911017c592
"hello!" →  d9b5f58f0b38198293971865a014e324
```

A single character change produces a completely different digest - this is called the **avalanche effect**.

## Usage

```bash
# hash a string
python md5.py "hello world"

# hash a file
python md5.py --file /path/to/file.txt

# pipe input
echo -n "hello" | python md5.py
```

Or import directly in Python:

```python
from md5 import md5

print(md5(b"hello"))
# 5d41402abc4b2a76b9719d911017c592
```

## How it works

MD5 processes input in four stages:

### 1. Padding
The message is padded so its length is a multiple of 512 bits (64 bytes). A `1` bit is appended, followed by zeros, followed by the original length as a 64-bit integer.

### 2. Chunking
The padded message is split into 64-byte chunks. This is the **Merkle-Damgard construction** - each chunk feeds into the next, so the final state depends on every bit of the input.

### 3. Compression (64 rounds per chunk)
Each chunk goes through 64 rounds split into four group of 16. Each group uses a different mixing function:

| Rounds | Function | Formula               |
|--------|----------|-----------------------|
| 1–16   | F        | `(B & C) \| (~B & D)` |
| 17–32  | G        | `(D & B) \| (~D & C)` |
| 33–48  | H        | `B ^ C ^ D`           |
| 49–64  | I        | `C ^ (B \| ~D)`       |


### 4. Digest
The four 32bit state words are packed as little-endian bytes and hex-encoded into the final 32-character digest.

## Project structure
 
```
md5-from-scratch/
├── README.md
├── LICENSE
├── .gitignore
├── md5.py              ← core implementation
├── conftest.py         ← makes pytest find md5.py
├── tests/
│   └── test_md5.py     ← validates against Python's hashlib
└── examples/
    └── usage.py        ← practical usage examples
```
 

## Why MD5 is broken
MD5 is **not safe** for any security-sensitive use. Do not use it for passwords, digital signatures, or certificates.

**Collision atrtacks (2004)** - researchers Wang and Yu showed two different inputs can produce the same hash. An attacker can craft a malicious file with the same MD5 as legitimate one.

**Too fast** - a modern GPU computes ~10 billion MD5 hashes per second, making brute-force attacks trivial.

**Rainbow tables** - precomputed lookup tables map common passwords to their MD5 hashes instantly.

## References

- [RFC 1321 — The MD5 Message-Digest Algorithm](https://www.ietf.org/rfc/rfc1321.txt)
- [Cryptanalysis of the MD5 — Wang & Yu, 2004](https://eprint.iacr.org/2004/199.pdf)
- [How MD5 works — Wikipedia](https://en.wikipedia.org/wiki/MD5)