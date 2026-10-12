# Zero-End Binary (ZEB), repo: Lossless

ZEB is an encoding in which every codeword ends in 0. Each byte `b` becomes the 9-bit symbol `2*b` (`abcdefgh → abcdefgh0`). Decoding is `code >> 1`, and odd values are rejected. It is lossless for all 256 byte values.

## Getting started

```bash
python3 zeb.py demo
python3 zeb.py bits "hello"
python3 zeb.py encode "hello" > hello.zeb
python3 zeb.py decode < hello.zeb       # or: python3 zeb.py decode <hex>
python3 test_zeb.py
```

## Python API

```python
from zeb import encode_text, decode_text, encode_bitstring, all_end_in_zero
```

Two forms are supported: the **bitstring** form (9-bit groups as text) and the **packed** form (two bytes per symbol, big-endian `2*b`).

## Files
`zeb.py` (library and CLI) and `test_zeb.py` (tests). There is no CI.

MIT License. Copyright (c) 2026 Joshua Almeida
