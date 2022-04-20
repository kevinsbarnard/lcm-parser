"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct


class header_t(object):
    __slots__ = ["publisher", "timestamp", "sequence"]

    def __init__(self):
        self.publisher = ""
        self.timestamp = 0.0
        self.sequence = 0

    def encode(self):
        buf = BytesIO()
        buf.write(header_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        __publisher_encoded = self.publisher.encode('utf-8')
        buf.write(struct.pack('>I', len(__publisher_encoded) + 1))
        buf.write(__publisher_encoded)
        buf.write(b"\0")
        buf.write(struct.pack(">dq", self.timestamp, self.sequence))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != header_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return header_t._decode_one(buf)

    decode = staticmethod(decode)

    def _decode_one(buf):
        self = header_t()
        __publisher_len = struct.unpack('>I', buf.read(4))[0]
        self.publisher = buf.read(__publisher_len)[:-1].decode('utf-8', 'replace')
        self.timestamp, self.sequence = struct.unpack(">dq", buf.read(16))
        return self

    _decode_one = staticmethod(_decode_one)

    _hash = None

    def _get_hash_recursive(parents):
        if header_t in parents: return 0
        tmphash = (0x628deda648a19ac5) & 0xffffffffffffffff
        tmphash = (((tmphash << 1) & 0xffffffffffffffff) + (tmphash >> 63)) & 0xffffffffffffffff
        return tmphash

    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if header_t._packed_fingerprint is None:
            header_t._packed_fingerprint = struct.pack(">Q", header_t._get_hash_recursive([]))
        return header_t._packed_fingerprint

    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)