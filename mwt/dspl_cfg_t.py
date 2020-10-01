"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class dspl_cfg_t(object):
    __slots__ = ["lout"]

    def __init__(self):
        self.lout = 0

    def encode(self):
        buf = BytesIO()
        buf.write(dspl_cfg_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">b", self.lout))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != dspl_cfg_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return dspl_cfg_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = dspl_cfg_t()
        self.lout = struct.unpack(">b", buf.read(1))[0]
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if dspl_cfg_t in parents: return 0
        tmphash = (0x90e9a182eec1a030) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff)  + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if dspl_cfg_t._packed_fingerprint is None:
            dspl_cfg_t._packed_fingerprint = struct.pack(">Q", dspl_cfg_t._get_hash_recursive([]))
        return dspl_cfg_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

