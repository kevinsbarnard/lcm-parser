"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

import mwt.header_t


class vehicle_cmd_t(object):
    __slots__ = ["header", "x", "y", "z", "phi", "theta", "psi"]

    def __init__(self):
        self.header = mwt.header_t()
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.phi = 0.0
        self.theta = 0.0
        self.psi = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(vehicle_cmd_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.header._get_packed_fingerprint() == mwt.header_t._get_packed_fingerprint()
        self.header._encode_one(buf)
        buf.write(struct.pack(">dddddd", self.x, self.y, self.z, self.phi, self.theta, self.psi))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != vehicle_cmd_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return vehicle_cmd_t._decode_one(buf)

    decode = staticmethod(decode)

    def _decode_one(buf):
        self = vehicle_cmd_t()
        self.header = mwt.header_t._decode_one(buf)
        self.x, self.y, self.z, self.phi, self.theta, self.psi = struct.unpack(">dddddd", buf.read(48))
        return self

    _decode_one = staticmethod(_decode_one)

    _hash = None

    def _get_hash_recursive(parents):
        if vehicle_cmd_t in parents: return 0
        newparents = parents + [vehicle_cmd_t]
        tmphash = (0xba86a0c54fd80a1f + mwt.header_t._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash = (((tmphash << 1) & 0xffffffffffffffff) + (tmphash >> 63)) & 0xffffffffffffffff
        return tmphash

    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if vehicle_cmd_t._packed_fingerprint is None:
            vehicle_cmd_t._packed_fingerprint = struct.pack(">Q", vehicle_cmd_t._get_hash_recursive([]))
        return vehicle_cmd_t._packed_fingerprint

    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)
