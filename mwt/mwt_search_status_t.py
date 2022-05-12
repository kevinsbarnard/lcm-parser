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

class mwt_search_status_t(object):
    __slots__ = ["header", "x_mode", "x_effort_cmd", "x_output", "y_mode", "y_effort_cmd", "y_output", "z_mode", "z_set_point", "z_goal", "z_moving", "z_effort_cmd", "z_output", "yaw_mode", "yaw_set_point", "yaw_goal", "yaw_moving", "yaw_effort_cmd", "yaw_output", "control_mode"]

    __typenames__ = ["mwt.header_t", "int32_t", "double", "double", "int32_t", "double", "double", "int32_t", "double", "double", "boolean", "double", "double", "int32_t", "double", "double", "boolean", "double", "double", "int32_t"]

    __dimensions__ = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    def __init__(self):
        self.header = mwt.header_t()
        self.x_mode = 0
        self.x_effort_cmd = 0.0
        self.x_output = 0.0
        self.y_mode = 0
        self.y_effort_cmd = 0.0
        self.y_output = 0.0
        self.z_mode = 0
        self.z_set_point = 0.0
        self.z_goal = 0.0
        self.z_moving = False
        self.z_effort_cmd = 0.0
        self.z_output = 0.0
        self.yaw_mode = 0
        self.yaw_set_point = 0.0
        self.yaw_goal = 0.0
        self.yaw_moving = False
        self.yaw_effort_cmd = 0.0
        self.yaw_output = 0.0
        self.control_mode = 0

    def encode(self):
        buf = BytesIO()
        buf.write(mwt_search_status_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.header._get_packed_fingerprint() == mwt.header_t._get_packed_fingerprint()
        self.header._encode_one(buf)
        buf.write(struct.pack(">iddiddiddbddiddbddi", self.x_mode, self.x_effort_cmd, self.x_output, self.y_mode, self.y_effort_cmd, self.y_output, self.z_mode, self.z_set_point, self.z_goal, self.z_moving, self.z_effort_cmd, self.z_output, self.yaw_mode, self.yaw_set_point, self.yaw_goal, self.yaw_moving, self.yaw_effort_cmd, self.yaw_output, self.control_mode))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != mwt_search_status_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return mwt_search_status_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = mwt_search_status_t()
        self.header = mwt.header_t._decode_one(buf)
        self.x_mode, self.x_effort_cmd, self.x_output, self.y_mode, self.y_effort_cmd, self.y_output, self.z_mode, self.z_set_point, self.z_goal = struct.unpack(">iddiddidd", buf.read(60))
        self.z_moving = bool(struct.unpack('b', buf.read(1))[0])
        self.z_effort_cmd, self.z_output, self.yaw_mode, self.yaw_set_point, self.yaw_goal = struct.unpack(">ddidd", buf.read(36))
        self.yaw_moving = bool(struct.unpack('b', buf.read(1))[0])
        self.yaw_effort_cmd, self.yaw_output, self.control_mode = struct.unpack(">ddi", buf.read(20))
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if mwt_search_status_t in parents: return 0
        newparents = parents + [mwt_search_status_t]
        tmphash = (0x83c48d6f82333212 + mwt.header_t._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if mwt_search_status_t._packed_fingerprint is None:
            mwt_search_status_t._packed_fingerprint = struct.pack(">Q", mwt_search_status_t._get_hash_recursive([]))
        return mwt_search_status_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", mwt_search_status_t._get_packed_fingerprint())[0]

