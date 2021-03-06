"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct


class controller_status_t(object):
    __slots__ = ["cmd", "measure", "integral", "derivative", "output", "kp", "ki", "kd", "tau", "output_scale"]

    def __init__(self):
        self.cmd = 0.0
        self.measure = 0.0
        self.integral = 0.0
        self.derivative = 0.0
        self.output = 0.0
        self.kp = 0.0
        self.ki = 0.0
        self.kd = 0.0
        self.tau = 0.0
        self.output_scale = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(controller_status_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(
            struct.pack(">dddddddddd", self.cmd, self.measure, self.integral, self.derivative, self.output, self.kp,
                        self.ki, self.kd, self.tau, self.output_scale))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != controller_status_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return controller_status_t._decode_one(buf)

    decode = staticmethod(decode)

    def _decode_one(buf):
        self = controller_status_t()
        self.cmd, self.measure, self.integral, self.derivative, self.output, self.kp, self.ki, self.kd, self.tau, self.output_scale = struct.unpack(
            ">dddddddddd", buf.read(80))
        return self

    _decode_one = staticmethod(_decode_one)

    _hash = None

    def _get_hash_recursive(parents):
        if controller_status_t in parents: return 0
        tmphash = (0xc07e52da64ca459e) & 0xffffffffffffffff
        tmphash = (((tmphash << 1) & 0xffffffffffffffff) + (tmphash >> 63)) & 0xffffffffffffffff
        return tmphash

    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if controller_status_t._packed_fingerprint is None:
            controller_status_t._packed_fingerprint = struct.pack(">Q", controller_status_t._get_hash_recursive([]))
        return controller_status_t._packed_fingerprint

    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)
