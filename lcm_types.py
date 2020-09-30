# lcm_types.py (lcm-parser)
from enum import IntEnum
from dataclasses import dataclass
import numpy as np


class PixelFormat(IntEnum):
    PIXEL_FORMAT_UYVY = 1498831189
    PIXEL_FORMAT_YUYV = 1448695129
    PIXEL_FORMAT_IYU1 = 827677001
    PIXEL_FORMAT_IYU2 = 844454217
    PIXEL_FORMAT_YUV420 = 842093913
    PIXEL_FORMAT_YUV411P = 1345401140
    PIXEL_FORMAT_I420 = 808596553
    PIXEL_FORMAT_NV12 = 842094158
    PIXEL_FORMAT_GRAY = 1497715271
    PIXEL_FORMAT_RGB = 859981650
    PIXEL_FORMAT_BGR = 861030210
    PIXEL_FORMAT_RGBA = 876758866
    PIXEL_FORMAT_BGRA = 877807426
    PIXEL_FORMAT_BAYER_BGGR = 825770306
    PIXEL_FORMAT_BAYER_GBRG = 844650584
    PIXEL_FORMAT_BAYER_GRBG = 861427800
    PIXEL_FORMAT_BAYER_RGGB = 878205016
    PIXEL_FORMAT_BE_BAYER16_BGGR = 826360386
    PIXEL_FORMAT_BE_BAYER16_GBRG = 843137602
    PIXEL_FORMAT_BE_BAYER16_GRBG = 859914818
    PIXEL_FORMAT_BE_BAYER16_RGGB = 876692034
    PIXEL_FORMAT_LE_BAYER16_BGGR = 826360396
    PIXEL_FORMAT_LE_BAYER16_GBRG = 843137612
    PIXEL_FORMAT_LE_BAYER16_GRBG = 859914828
    PIXEL_FORMAT_LE_BAYER16_RGGB = 876692044
    PIXEL_FORMAT_MJPEG = 1196444237
    PIXEL_FORMAT_BE_GRAY16 = 357
    PIXEL_FORMAT_LE_GRAY16 = 909199180
    PIXEL_FORMAT_BE_RGB16 = 358
    PIXEL_FORMAT_LE_RGB16 = 1279412050
    PIXEL_FORMAT_BE_SIGNED_GRAY16 = 359
    PIXEL_FORMAT_BE_SIGNED_RGB16 = 360
    PIXEL_FORMAT_FLOAT_GRAY32 = 842221382
    PIXEL_FORMAT_INVALID = -2
    PIXEL_FORMAT_ANY = -1


@dataclass
class Image:
    utime: int = None
    width: int = None
    height: int = None
    row_stride: int = None
    pixelformat: PixelFormat = None
    size: int = None
    data: np.ndarray = None

    @staticmethod
    def read_from_bytes(f):
        utime = int.from_bytes(f.read(8), 'big')
        width = int.from_bytes(f.read(4), 'big')
        height = int.from_bytes(f.read(4), 'big')
        row_stride = int.from_bytes(f.read(4), 'big')
        pixelformat = PixelFormat(int.from_bytes(f.read(4), 'big'))
        size = int.from_bytes(f.read(4), 'big')
        data_bytes = f.read(size)
        data_flat = np.frombuffer(data_bytes, dtype=np.ubyte)  # Is data always ubyte?
        depth = size // (width * height)  # Bit of a hack
        data = np.reshape((height, width, depth))

        return Image(utime, width, height, row_stride, pixelformat, size, data)
