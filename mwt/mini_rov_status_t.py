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

class mini_rov_status_t(object):
    __slots__ = ["header", "auto_head", "auto_vert", "adv_nav", "auto_head_sp", "auto_depth_sp", "x_pilot", "y_pilot", "z_pilot", "yaw_pilot", "x_effort", "y_effort", "z_effort", "yaw_effort", "f1_thrust", "f2_thrust", "f3_thrust", "f4_thrust", "fz_thrust", "f1_limit", "f2_limit", "f3_limit", "f4_limit", "fz_limit"]

    __typenames__ = ["mwt.header_t", "boolean", "boolean", "boolean", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "int16_t", "int16_t", "int16_t", "int16_t", "int16_t"]

    __dimensions__ = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    def __init__(self):
        self.header = mwt.header_t()
        self.auto_head = False
        self.auto_vert = False
        self.adv_nav = False
        self.auto_head_sp = 0.0
        self.auto_depth_sp = 0.0
        self.x_pilot = 0.0
        self.y_pilot = 0.0
        self.z_pilot = 0.0
        self.yaw_pilot = 0.0
        self.x_effort = 0.0
        self.y_effort = 0.0
        self.z_effort = 0.0
        self.yaw_effort = 0.0
        self.f1_thrust = 0.0
        self.f2_thrust = 0.0
        self.f3_thrust = 0.0
        self.f4_thrust = 0.0
        self.fz_thrust = 0.0
        self.f1_limit = 0
        self.f2_limit = 0
        self.f3_limit = 0
        self.f4_limit = 0
        self.fz_limit = 0

    def encode(self):
        buf = BytesIO()
        buf.write(mini_rov_status_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.header._get_packed_fingerprint() == mwt.header_t._get_packed_fingerprint()
        self.header._encode_one(buf)
        buf.write(struct.pack(">bbbdddddddddddddddhhhhh", self.auto_head, self.auto_vert, self.adv_nav, self.auto_head_sp, self.auto_depth_sp, self.x_pilot, self.y_pilot, self.z_pilot, self.yaw_pilot, self.x_effort, self.y_effort, self.z_effort, self.yaw_effort, self.f1_thrust, self.f2_thrust, self.f3_thrust, self.f4_thrust, self.fz_thrust, self.f1_limit, self.f2_limit, self.f3_limit, self.f4_limit, self.fz_limit))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != mini_rov_status_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return mini_rov_status_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = mini_rov_status_t()
        self.header = mwt.header_t._decode_one(buf)
        self.auto_head = bool(struct.unpack('b', buf.read(1))[0])
        self.auto_vert = bool(struct.unpack('b', buf.read(1))[0])
        self.adv_nav = bool(struct.unpack('b', buf.read(1))[0])
        self.auto_head_sp, self.auto_depth_sp, self.x_pilot, self.y_pilot, self.z_pilot, self.yaw_pilot, self.x_effort, self.y_effort, self.z_effort, self.yaw_effort, self.f1_thrust, self.f2_thrust, self.f3_thrust, self.f4_thrust, self.fz_thrust, self.f1_limit, self.f2_limit, self.f3_limit, self.f4_limit, self.fz_limit = struct.unpack(">dddddddddddddddhhhhh", buf.read(130))
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if mini_rov_status_t in parents: return 0
        newparents = parents + [mini_rov_status_t]
        tmphash = (0x84f537ed87e9e45a + mwt.header_t._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if mini_rov_status_t._packed_fingerprint is None:
            mini_rov_status_t._packed_fingerprint = struct.pack(">Q", mini_rov_status_t._get_hash_recursive([]))
        return mini_rov_status_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", mini_rov_status_t._get_packed_fingerprint())[0]

