"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

import mwt.gain_scale_status_t

import mwt.header_t

import mwt.filter_status_t

import mwt.controller_status_t

import mwt.trajectory_status_t


class mwt_control_status_t(object):
    __slots__ = ["header", "range_control", "lateral_control", "vertical_control", "bearing_control", "range_traj",
                 "lateral_traj", "vertical_traj", "bearing_traj", "range_filter", "lateral_filter", "vertical_filter",
                 "bearing_filter", "range_gs_filter", "heading_gs_filter", "bearing_gs_filter", "lateral_gs",
                 "bearing_gs", "is_pilot_enabled", "is_control_enabled", "is_x_effort_enabled", "is_y_effort_enabled",
                 "is_z_effort_enabled", "is_psi_effort_enabled", "control_exec_ms", "other_exec_ms", "percent_idle",
                 "missed_updates"]

    def __init__(self):
        self.header = mwt.header_t()
        self.range_control = mwt.controller_status_t()
        self.lateral_control = mwt.controller_status_t()
        self.vertical_control = mwt.controller_status_t()
        self.bearing_control = mwt.controller_status_t()
        self.range_traj = mwt.trajectory_status_t()
        self.lateral_traj = mwt.trajectory_status_t()
        self.vertical_traj = mwt.trajectory_status_t()
        self.bearing_traj = mwt.trajectory_status_t()
        self.range_filter = mwt.filter_status_t()
        self.lateral_filter = mwt.filter_status_t()
        self.vertical_filter = mwt.filter_status_t()
        self.bearing_filter = mwt.filter_status_t()
        self.range_gs_filter = mwt.filter_status_t()
        self.heading_gs_filter = mwt.filter_status_t()
        self.bearing_gs_filter = mwt.filter_status_t()
        self.lateral_gs = mwt.gain_scale_status_t()
        self.bearing_gs = mwt.gain_scale_status_t()
        self.is_pilot_enabled = False
        self.is_control_enabled = False
        self.is_x_effort_enabled = False
        self.is_y_effort_enabled = False
        self.is_z_effort_enabled = False
        self.is_psi_effort_enabled = False
        self.control_exec_ms = 0.0
        self.other_exec_ms = 0.0
        self.percent_idle = 0.0
        self.missed_updates = 0

    def encode(self):
        buf = BytesIO()
        buf.write(mwt_control_status_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        assert self.header._get_packed_fingerprint() == mwt.header_t._get_packed_fingerprint()
        self.header._encode_one(buf)
        assert self.range_control._get_packed_fingerprint() == mwt.controller_status_t._get_packed_fingerprint()
        self.range_control._encode_one(buf)
        assert self.lateral_control._get_packed_fingerprint() == mwt.controller_status_t._get_packed_fingerprint()
        self.lateral_control._encode_one(buf)
        assert self.vertical_control._get_packed_fingerprint() == mwt.controller_status_t._get_packed_fingerprint()
        self.vertical_control._encode_one(buf)
        assert self.bearing_control._get_packed_fingerprint() == mwt.controller_status_t._get_packed_fingerprint()
        self.bearing_control._encode_one(buf)
        assert self.range_traj._get_packed_fingerprint() == mwt.trajectory_status_t._get_packed_fingerprint()
        self.range_traj._encode_one(buf)
        assert self.lateral_traj._get_packed_fingerprint() == mwt.trajectory_status_t._get_packed_fingerprint()
        self.lateral_traj._encode_one(buf)
        assert self.vertical_traj._get_packed_fingerprint() == mwt.trajectory_status_t._get_packed_fingerprint()
        self.vertical_traj._encode_one(buf)
        assert self.bearing_traj._get_packed_fingerprint() == mwt.trajectory_status_t._get_packed_fingerprint()
        self.bearing_traj._encode_one(buf)
        assert self.range_filter._get_packed_fingerprint() == mwt.filter_status_t._get_packed_fingerprint()
        self.range_filter._encode_one(buf)
        assert self.lateral_filter._get_packed_fingerprint() == mwt.filter_status_t._get_packed_fingerprint()
        self.lateral_filter._encode_one(buf)
        assert self.vertical_filter._get_packed_fingerprint() == mwt.filter_status_t._get_packed_fingerprint()
        self.vertical_filter._encode_one(buf)
        assert self.bearing_filter._get_packed_fingerprint() == mwt.filter_status_t._get_packed_fingerprint()
        self.bearing_filter._encode_one(buf)
        assert self.range_gs_filter._get_packed_fingerprint() == mwt.filter_status_t._get_packed_fingerprint()
        self.range_gs_filter._encode_one(buf)
        assert self.heading_gs_filter._get_packed_fingerprint() == mwt.filter_status_t._get_packed_fingerprint()
        self.heading_gs_filter._encode_one(buf)
        assert self.bearing_gs_filter._get_packed_fingerprint() == mwt.filter_status_t._get_packed_fingerprint()
        self.bearing_gs_filter._encode_one(buf)
        assert self.lateral_gs._get_packed_fingerprint() == mwt.gain_scale_status_t._get_packed_fingerprint()
        self.lateral_gs._encode_one(buf)
        assert self.bearing_gs._get_packed_fingerprint() == mwt.gain_scale_status_t._get_packed_fingerprint()
        self.bearing_gs._encode_one(buf)
        buf.write(struct.pack(">bbbbbbdddq", self.is_pilot_enabled, self.is_control_enabled, self.is_x_effort_enabled,
                              self.is_y_effort_enabled, self.is_z_effort_enabled, self.is_psi_effort_enabled,
                              self.control_exec_ms, self.other_exec_ms, self.percent_idle, self.missed_updates))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != mwt_control_status_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return mwt_control_status_t._decode_one(buf)

    decode = staticmethod(decode)

    def _decode_one(buf):
        self = mwt_control_status_t()
        self.header = mwt.header_t._decode_one(buf)
        self.range_control = mwt.controller_status_t._decode_one(buf)
        self.lateral_control = mwt.controller_status_t._decode_one(buf)
        self.vertical_control = mwt.controller_status_t._decode_one(buf)
        self.bearing_control = mwt.controller_status_t._decode_one(buf)
        self.range_traj = mwt.trajectory_status_t._decode_one(buf)
        self.lateral_traj = mwt.trajectory_status_t._decode_one(buf)
        self.vertical_traj = mwt.trajectory_status_t._decode_one(buf)
        self.bearing_traj = mwt.trajectory_status_t._decode_one(buf)
        self.range_filter = mwt.filter_status_t._decode_one(buf)
        self.lateral_filter = mwt.filter_status_t._decode_one(buf)
        self.vertical_filter = mwt.filter_status_t._decode_one(buf)
        self.bearing_filter = mwt.filter_status_t._decode_one(buf)
        self.range_gs_filter = mwt.filter_status_t._decode_one(buf)
        self.heading_gs_filter = mwt.filter_status_t._decode_one(buf)
        self.bearing_gs_filter = mwt.filter_status_t._decode_one(buf)
        self.lateral_gs = mwt.gain_scale_status_t._decode_one(buf)
        self.bearing_gs = mwt.gain_scale_status_t._decode_one(buf)
        self.is_pilot_enabled = bool(struct.unpack('b', buf.read(1))[0])
        self.is_control_enabled = bool(struct.unpack('b', buf.read(1))[0])
        self.is_x_effort_enabled = bool(struct.unpack('b', buf.read(1))[0])
        self.is_y_effort_enabled = bool(struct.unpack('b', buf.read(1))[0])
        self.is_z_effort_enabled = bool(struct.unpack('b', buf.read(1))[0])
        self.is_psi_effort_enabled = bool(struct.unpack('b', buf.read(1))[0])
        self.control_exec_ms, self.other_exec_ms, self.percent_idle, self.missed_updates = struct.unpack(">dddq",
                                                                                                         buf.read(32))
        return self

    _decode_one = staticmethod(_decode_one)

    _hash = None

    def _get_hash_recursive(parents):
        if mwt_control_status_t in parents: return 0
        newparents = parents + [mwt_control_status_t]
        tmphash = (0xcfdb15991e731c60 + mwt.header_t._get_hash_recursive(
            newparents) + mwt.controller_status_t._get_hash_recursive(
            newparents) + mwt.controller_status_t._get_hash_recursive(
            newparents) + mwt.controller_status_t._get_hash_recursive(
            newparents) + mwt.controller_status_t._get_hash_recursive(
            newparents) + mwt.trajectory_status_t._get_hash_recursive(
            newparents) + mwt.trajectory_status_t._get_hash_recursive(
            newparents) + mwt.trajectory_status_t._get_hash_recursive(
            newparents) + mwt.trajectory_status_t._get_hash_recursive(
            newparents) + mwt.filter_status_t._get_hash_recursive(newparents) + mwt.filter_status_t._get_hash_recursive(
            newparents) + mwt.filter_status_t._get_hash_recursive(newparents) + mwt.filter_status_t._get_hash_recursive(
            newparents) + mwt.filter_status_t._get_hash_recursive(newparents) + mwt.filter_status_t._get_hash_recursive(
            newparents) + mwt.filter_status_t._get_hash_recursive(
            newparents) + mwt.gain_scale_status_t._get_hash_recursive(
            newparents) + mwt.gain_scale_status_t._get_hash_recursive(newparents)) & 0xffffffffffffffff
        tmphash = (((tmphash << 1) & 0xffffffffffffffff) + (tmphash >> 63)) & 0xffffffffffffffff
        return tmphash

    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if mwt_control_status_t._packed_fingerprint is None:
            mwt_control_status_t._packed_fingerprint = struct.pack(">Q", mwt_control_status_t._get_hash_recursive([]))
        return mwt_control_status_t._packed_fingerprint

    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)
