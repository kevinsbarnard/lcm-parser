"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class supervisor_cfg_t_new(object):
    __slots__ = ["state_number", "max_target_jump", "max_target_step", "min_track_score", "min_track_iou", "range_setpoint", "range_deadband", "bearing_deadband", "z_deadband", "acquire_max_range", "acquire_max_bearing", "acquire_max_z", "track_max_range", "track_max_bearing", "track_max_z", "track_range_gain", "track_bearing_gain", "track_z_gain", "acquire_range_gain", "acquire_bearing_gain", "acquire_z_gain", "bearing_setpoint", "vertical_setpoint", "search_timeout", "acquire_timeout", "track_timeout", "track_duration", "class_label_history", "ignore_class_label_in_track", "control_mode", "state_name", "target_class", "acquire_mode", "track_mode", "classes_to_track"]

    __typenames__ = ["double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", "string", "string", "string", "string", "string", "string"]

    __dimensions__ = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    def __init__(self):
        self.state_number = 0.0
        self.max_target_jump = 0.0
        self.max_target_step = 0.0
        self.min_track_score = 0.0
        self.min_track_iou = 0.0
        self.range_setpoint = 0.0
        self.range_deadband = 0.0
        self.bearing_deadband = 0.0
        self.z_deadband = 0.0
        self.acquire_max_range = 0.0
        self.acquire_max_bearing = 0.0
        self.acquire_max_z = 0.0
        self.track_max_range = 0.0
        self.track_max_bearing = 0.0
        self.track_max_z = 0.0
        self.track_range_gain = 0.0
        self.track_bearing_gain = 0.0
        self.track_z_gain = 0.0
        self.acquire_range_gain = 0.0
        self.acquire_bearing_gain = 0.0
        self.acquire_z_gain = 0.0
        self.bearing_setpoint = 0.0
        self.vertical_setpoint = 0.0
        self.search_timeout = 0.0
        self.acquire_timeout = 0.0
        self.track_timeout = 0.0
        self.track_duration = 0.0
        self.class_label_history = 0.0
        self.ignore_class_label_in_track = 0.0
        self.control_mode = ""
        self.state_name = ""
        self.target_class = ""
        self.acquire_mode = ""
        self.track_mode = ""
        self.classes_to_track = ""

    def encode(self):
        buf = BytesIO()
        buf.write(supervisor_cfg_t_new._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">ddddddddddddddddddddddddddddd", self.state_number, self.max_target_jump, self.max_target_step, self.min_track_score, self.min_track_iou, self.range_setpoint, self.range_deadband, self.bearing_deadband, self.z_deadband, self.acquire_max_range, self.acquire_max_bearing, self.acquire_max_z, self.track_max_range, self.track_max_bearing, self.track_max_z, self.track_range_gain, self.track_bearing_gain, self.track_z_gain, self.acquire_range_gain, self.acquire_bearing_gain, self.acquire_z_gain, self.bearing_setpoint, self.vertical_setpoint, self.search_timeout, self.acquire_timeout, self.track_timeout, self.track_duration, self.class_label_history, self.ignore_class_label_in_track))
        __control_mode_encoded = self.control_mode.encode('utf-8')
        buf.write(struct.pack('>I', len(__control_mode_encoded)+1))
        buf.write(__control_mode_encoded)
        buf.write(b"\0")
        __state_name_encoded = self.state_name.encode('utf-8')
        buf.write(struct.pack('>I', len(__state_name_encoded)+1))
        buf.write(__state_name_encoded)
        buf.write(b"\0")
        __target_class_encoded = self.target_class.encode('utf-8')
        buf.write(struct.pack('>I', len(__target_class_encoded)+1))
        buf.write(__target_class_encoded)
        buf.write(b"\0")
        __acquire_mode_encoded = self.acquire_mode.encode('utf-8')
        buf.write(struct.pack('>I', len(__acquire_mode_encoded)+1))
        buf.write(__acquire_mode_encoded)
        buf.write(b"\0")
        __track_mode_encoded = self.track_mode.encode('utf-8')
        buf.write(struct.pack('>I', len(__track_mode_encoded)+1))
        buf.write(__track_mode_encoded)
        buf.write(b"\0")
        __classes_to_track_encoded = self.classes_to_track.encode('utf-8')
        buf.write(struct.pack('>I', len(__classes_to_track_encoded)+1))
        buf.write(__classes_to_track_encoded)
        buf.write(b"\0")

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
            buf.read(8)
        # if buf.read(8) != supervisor_cfg_t_new._get_packed_fingerprint():
        #     raise ValueError("Decode error")
        return supervisor_cfg_t_new._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = supervisor_cfg_t_new()
        self.state_number, self.max_target_jump, self.max_target_step, self.min_track_score, self.min_track_iou, self.range_setpoint, self.range_deadband, self.bearing_deadband, self.z_deadband, self.acquire_max_range, self.acquire_max_bearing, self.acquire_max_z, self.track_max_range, self.track_max_bearing, self.track_max_z, self.track_range_gain, self.track_bearing_gain, self.track_z_gain, self.acquire_range_gain, self.acquire_bearing_gain, self.acquire_z_gain, self.bearing_setpoint, self.vertical_setpoint, self.search_timeout, self.acquire_timeout, self.track_timeout, self.track_duration, self.class_label_history, self.ignore_class_label_in_track = struct.unpack(">ddddddddddddddddddddddddddddd", buf.read(232))
        # self.state_number, self.max_target_jump, self.max_target_step, self.min_track_score, self.min_track_iou, self.range_setpoint, self.range_deadband, self.bearing_deadband, self.z_deadband, self.acquire_max_range, self.acquire_max_bearing, self.acquire_max_z, self.track_max_range, self.track_max_bearing, self.track_max_z, self.track_range_gain, self.track_bearing_gain, self.track_z_gain, self.acquire_range_gain, self.acquire_bearing_gain, self.acquire_z_gain, self.bearing_setpoint, self.vertical_setpoint, self.search_timeout, self.acquire_timeout, self.track_timeout, self.track_duration = struct.unpack(
        #     ">ddddddddddddddddddddddddddd", buf.read(216))
        __control_mode_len = struct.unpack('>I', buf.read(4))[0]
        self.control_mode = buf.read(__control_mode_len)[:-1].decode('utf-8', 'replace')
        __state_name_len = struct.unpack('>I', buf.read(4))[0]
        self.state_name = buf.read(__state_name_len)[:-1].decode('utf-8', 'replace')
        __target_class_len = struct.unpack('>I', buf.read(4))[0]
        self.target_class = buf.read(__target_class_len)[:-1].decode('utf-8', 'replace')
        __acquire_mode_len = struct.unpack('>I', buf.read(4))[0]
        self.acquire_mode = buf.read(__acquire_mode_len)[:-1].decode('utf-8', 'replace')
        __track_mode_len = struct.unpack('>I', buf.read(4))[0]
        self.track_mode = buf.read(__track_mode_len)[:-1].decode('utf-8', 'replace')
        __classes_to_track_len = struct.unpack('>I', buf.read(4))[0]
        self.classes_to_track = buf.read(__classes_to_track_len)[:-1].decode('utf-8', 'replace')
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if supervisor_cfg_t_new in parents: return 0
        tmphash = (0x9ae3f23451601a04) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if supervisor_cfg_t_new._packed_fingerprint is None:
            supervisor_cfg_t_new._packed_fingerprint = struct.pack(">Q", supervisor_cfg_t_new._get_hash_recursive([]))
        return supervisor_cfg_t_new._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", supervisor_cfg_t_new._get_packed_fingerprint())[0]
