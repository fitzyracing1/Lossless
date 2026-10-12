# Zero-End Binary (ZEB)

Encoding system where **every binary codeword ends in 0**.

## Rule

| Direction | Operation | Binary effect |
|-----------|-----------|----------------|
| Encode    | `code = byte << 1` (`2 * byte`) | append a trailing `0` |
| Decode    | `byte = code >> 1` (`code // 2`) | drop the trailing `0` |

Each original byte becomes a 9-bit symbol:

```
abcdefgh  →  abcdefgh0
```

Every symbol is even. Concatenated streams are groups of 9 bits, each group ending in `0`.

## Why this works

- Unique and lossless for all 256 byte values (`0..255` → `0, 2, 4, …, 510`).
- Odd values are illegal and rejected on decode.
- The trailing `0` is a hard invariant, not a checksum.

## Usage

```python
from zeb import encode_text, decode_text, encode_bitstring, all_end_in_zero

packed = encode_text("hello")
print(decode_text(packed))          # hello

bits = encode_bitstring(b"hello")
print(all_end_in_zero(bits))        # True
```

CLI:

```bash
python3 zeb.py demo
python3 zeb.py bits "hello"
python3 zeb.py encode "hello" > hello.zeb
```

## Forms

1. **Bitstring** — 9-bit groups, human readable, every group ends in `0`.
2. **Packed** — two bytes per symbol holding the even integer `2 * b` (big-endian).

## Limits

- Packed size is `2n` bytes for `n` input bytes.
- Bitstring length is `9n` bits.
- Not a compression format. It is an invariant encoding.

## Version

1.0.0

## Documentation

- In-repo docs: [docs/](docs/index.md)
- Wiki: [https://github.com/fitzyracing1/Lossless/wiki](https://github.com/fitzyracing1/Lossless/wiki)
