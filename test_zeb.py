#!/usr/bin/env python3
import unittest
from zeb import (
    encode_bytes,
    decode_bytes,
    encode_text,
    decode_text,
    encode_bitstring,
    decode_bitstring,
    all_end_in_zero,
)


class TestZEB(unittest.TestCase):
    def test_roundtrip_ascii(self):
        s = "Zero-End Binary"
        self.assertEqual(decode_text(encode_text(s)), s)

    def test_roundtrip_all_bytes(self):
        data = bytes(range(256))
        self.assertEqual(decode_bytes(encode_bytes(data)), data)

    def test_bitstring_ends_zero(self):
        bits = encode_bitstring(b"abc")
        self.assertTrue(all(g.endswith("0") for g in [bits[i:i+9] for i in range(0, len(bits), 9)]))
        self.assertTrue(all_end_in_zero(bits))
        self.assertEqual(decode_bitstring(bits), b"abc")

    def test_odd_rejected(self):
        with self.assertRaises(ValueError):
            decode_bytes(b"\x00\x01")

    def test_empty(self):
        self.assertEqual(encode_bytes(b""), b"")
        self.assertEqual(decode_bytes(b""), b"")
        self.assertEqual(encode_bitstring(b""), "")


if __name__ == "__main__":
    unittest.main()
