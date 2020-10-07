"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct


class gain_scale_status_t(object):
    __slots__ = ["enabled", "kp_in", "ki_in", "kd_in", "kp_out", "ki_out", "kd_out"]

    def __init__(self):
        self.enabled = False
        self.kp_in = 0.0
        self.ki_in = 0.0
        self.kd_in = 0.0
        self.kp_out = 0.0
        self.ki_out = 0.0
        self.kd_out = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(gain_scale_status_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">bdddddd", self.enabled, self.kp_in, self.ki_in, self.kd_in, self.kp_out, self.ki_out,
                              self.kd_out))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != gain_scale_status_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return gain_scale_status_t._decode_one(buf)

    decode = staticmethod(decode)

    def _decode_one(buf):
        self = gain_scale_status_t()
        self.enabled = bool(struct.unpack('b', buf.read(1))[0])
        self.kp_in, self.ki_in, self.kd_in, self.kp_out, self.ki_out, self.kd_out = struct.unpack(">dddddd",
                                                                                                  buf.read(48))
        return self

    _decode_one = staticmethod(_decode_one)

    _hash = None

    def _get_hash_recursive(parents):
        if gain_scale_status_t in parents: return 0
        tmphash = (0x58056ad4bf4807c7) & 0xffffffffffffffff
        tmphash = (((tmphash << 1) & 0xffffffffffffffff) + (tmphash >> 63)) & 0xffffffffffffffff
        return tmphash

    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if gain_scale_status_t._packed_fingerprint is None:
            gain_scale_status_t._packed_fingerprint = struct.pack(">Q", gain_scale_status_t._get_hash_recursive([]))
        return gain_scale_status_t._packed_fingerprint

    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)
