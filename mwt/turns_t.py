"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class turns_t(object):
    __slots__ = ["turns"]

    __typenames__ = ["double"]

    __dimensions__ = [None]

    def __init__(self):
        self.turns = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(turns_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">d", self.turns))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != turns_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return turns_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = turns_t()
        self.turns = struct.unpack(">d", buf.read(8))[0]
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if turns_t in parents: return 0
        tmphash = (0x4cab85a1b2ae8a48) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if turns_t._packed_fingerprint is None:
            turns_t._packed_fingerprint = struct.pack(">Q", turns_t._get_hash_recursive([]))
        return turns_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", turns_t._get_packed_fingerprint())[0]

