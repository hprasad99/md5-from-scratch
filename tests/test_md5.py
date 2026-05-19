import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from md5 import md5

cases = [b"", b"hello", b"hello world", b"a" * 1000]

for case in cases:
    assert md5(case) == hashlib.md5(case).hexdigest()
    print(f"PASS: {case[:20]}")
