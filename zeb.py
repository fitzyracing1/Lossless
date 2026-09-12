#!/usr/bin/env python3
"""Zero-End Binary (ZEB)

Every encoded symbol is even, so its binary representation always ends in 0.

Encode: each input byte b becomes 2*b (left shift 1).
Decode: each even codeword c becomes c // 2 (right shift 1).

Bit form: 8 data bits + trailing 0  =>  9-bit symbols, all ending in 0.
"""

from __future__ import annotations


VERSION = "1.0.0"


def encode_bytes(data: bytes) -> bytes:
    """Map each byte b to two bytes holding 2*b (0..510, always even)."""
    out = bytearray()
    for b in data:
        v = b << 1
        out.append((v >> 8) & 0xFF)
        out.append(v & 0xFF)
    return bytes(out)


def decode_bytes(data: bytes) -> bytes:
    """Inverse of encode_bytes. Raises ValueError if a codeword is odd."""
    if len(data) % 2 != 0:
        raise ValueError("ZEB packed form must have even length")
    out = bytearray()
    for i in range(0, len(data), 2):
        v = (data[i] << 8) | data[i + 1]
        if v & 1:
            raise ValueError(f"codeword at {i} ends in 1 (odd): {v}")
        if v > 510:
            raise ValueError(f"codeword at {i} out of range: {v}")
        out.append(v >> 1)
    return bytes(out)


def encode_text(text: str, encoding: str = "utf-8") -> bytes:
    return encode_bytes(text.encode(encoding))


def decode_text(data: bytes, encoding: str = "utf-8") -> str:
    return decode_bytes(data).decode(encoding)


def encode_bitstring(data: bytes) -> str:
    """9-bit groups: original 8 bits plus a trailing 0."""
    parts = []
    for b in data:
        parts.append(format(b, "08b") + "0")
    return "".join(parts)


def decode_bitstring(bits: str) -> bytes:
    bits = "".join(bits.split())
    if len(bits) % 9 != 0:
        raise ValueError("bitstring length must be a multiple of 9")
    out = bytearray()
    for i in range(0, len(bits), 9):
        group = bits[i : i + 9]
        if group[-1] != "0":
            raise ValueError(f"group at bit {i} does not end in 0: {group}")
        out.append(int(group[:8], 2))
    return bytes(out)


def all_end_in_zero(bits: str) -> bool:
    bits = "".join(bits.split())
    if not bits or len(bits) % 9 != 0:
        return False
    return all(bits[i + 8] == "0" for i in range(0, len(bits), 9))


def _demo() -> None:
    sample = "ZEB ends in 0"
    packed = encode_text(sample)
    bits = encode_bitstring(sample.encode())
    recovered = decode_text(packed)
    print("text     :", sample)
    print("packed   :", packed.hex())
    print("bits     :", " ".join(bits[i : i + 9] for i in range(0, len(bits), 9)))
    print("all end 0:", all_end_in_zero(bits))
    print("decoded  :", recovered)
    assert recovered == sample
    assert decode_bitstring(bits) == sample.encode()


if __name__ == "__main__":
    import argparse
    import sys

    p = argparse.ArgumentParser(description="Zero-End Binary encoder")
    p.add_argument("mode", choices=["encode", "decode", "bits", "demo"])
    p.add_argument("text", nargs="?", default="")
    args = p.parse_args()

    if args.mode == "demo":
        _demo()
    elif args.mode == "encode":
        sys.stdout.buffer.write(encode_text(args.text))
    elif args.mode == "decode":
        raw = sys.stdin.buffer.read() if not args.text else bytes.fromhex(args.text)
        print(decode_text(raw), end="")
    elif args.mode == "bits":
        print(encode_bitstring(args.text.encode()))
