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

## Why MD5 is broken

## References
